#!/usr/bin/env python
import configparser
import syslog
import asyncio
import sys
import email
import email.policy
import requests
import smtplib
from aiosmtpd.controller import Controller
from aiosmtpd.handlers import Message

class LMTPController(Controller):
    def factory(self):
        return aiosmptd.smtp.SMTP(self.handler, enable_SMTPUTF8=self.enable_SMTPUTF8)

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
        h = {'IP': '127.0.0.1'}
        r = requests.post('http://localhost:11333/checkv2', data=message.as_bytes(),
                headers = h)
        j = r.json()
        print(j)
        message['DKIM-Signature'] = j['dkim-signature'].replace('\r', '').replace('\n', '')
        with smtplib.SMTP('localhost', 2525) as s:
            s.send_message(message)


syslog.openlog(logoption=syslog.LOG_PID, facility=syslog.LOG_MAIL)
syslog.syslog("Starting pyrelay-rspamd")

if len(sys.argv) < 2:
    syslog.syslog(syslog.LOG_ERR, "No configuration file specified")
    sys.exit(2)

config = configparser.ConfigParser()
try:
    config = configparser.ConfigParser().read_file(open(sys.argv[1]))
except configparser.Error as err:
    syslog.syslog(syslog.LOG_ERR, "Unable to parse configuration: {}".format(err))
    sys.exit(2)
#controller = LMTPController(Handler(),hostname="localhost", port=8025)
controller = Controller(Handler())
controller.start()
print("Hit enter to stop")
sys.stdin.readline()
controller.stop()
