#!/usr/bin/env python
import configparser
import syslog
import asyncio
import sys
import email
import email.policy
import requests
import smtplib
import logging
import logging.handlers
import socket
from aiosmtpd.controller import Controller
from aiosmtpd.handlers import Message
from aiosmtpd.smtp import SMTP

class Handler(Message):
    def prepare_message(self, session, envelope):
        # If the server was created with decode_data True, then data will be a
        # str, otherwise it will be bytes.
        data = envelope.content
        if isinstance(data, bytes):
            message = email.message_from_bytes(data, policy=email.policy.SMTP)
        else:
            assert isinstance(data, str), (
              'Expected str or bytes, got {}'.format(type(data)))
            message = email.message_from_string(data, policy=email.policy.SMTP)
        return message

    def handle_message(self, message):
        r = requests.post('http://localhost:11333/checkv2', data=message.as_bytes(),
                headers = dict(config.items('HEADERS')))
        j = r.json()

        if 'dkim-signature' not in j:
            logging.warning('rspamd did not return a signature for message {}'.format(message.get('Message-ID', '(Message-ID not found)')))
        else:
            message['DKIM-Signature'] = j['dkim-signature'].replace('\r', '').replace('\n', '')
        with smtplib.SMTP('localhost', 2525) as s:
            s.send_message(message)

    async def handle_exception(self, err):
        logging.error("Unable to relay message: {}".format(err))
        return "554 Unable to relay mail"

global config
if len(sys.argv) < 2:
    print("No configuration file specified", file=os.stderr)
    sys.exit(2)
config = configparser.ConfigParser()
try:
    config.read_file(open(sys.argv[1]))
except configparser.Error as err:
    print("Unable to parse configuration: {}".format(err), file=os.stderr)
    sys.exit(2)

if 'LOG' in config:
    logger = logging.getLogger()
    handler = {'syslog': logging.handlers.SysLogHandler(facility='mail',address='/dev/log'),
                'none': logging.NullHandler(),
                'file': logging.handlers.TimedRotatingFileHandler(config['LOG'].get('file', 'pyrelay-rspamd.log'), when='midnight')
              }.get(config['LOG'].get('type'), logging.StreamHandler())
    if isinstance(handler, logging.handlers.SysLogHandler):
        handler.ident = "pyrelay-rspamd: "
    else:
        fmt = logging.Formatter(fmt='{asctime}:{levelname}: {message}', style='{')
        handler.setFormatter(fmt)
    logger.addHandler(handler)
    logger.setLevel(config['LOG'].get('level', 'INFO'))
else:
    logging.basicConfig()

logging.info("Starting pyrelay-rspamd")

controller = Controller(Handler())
controller.start()
print("Hit enter to stop")
sys.stdin.readline()
controller.stop()
