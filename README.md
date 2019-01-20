# pyrelay-rspamd

A simple python script to put a dkim signature on an
email using rspamd and then forward it via SMTP.

## Why?

Many guides for OpenSMTPD have you install both rspamd and
dkimfilter. However, rspamd is perfectly capable of putting
dkim signatures on outgoing mail. Why install all that when
all you need is a small script to make rspamd to the work?

## Requirements

* Python 3.7+ (sorry, I use `asyncio.run()` )
* requests
* aiosmtp

## Configuration

```
$ sudo mv pyrelay-rspamd.conf.example /etc/pyrelay-rspamd.conf
$ sudo cat rspamd-settings.local.example >> /etc/rspamd/local.d/settings.conf
$ sudo vi /etc/pyrelay-rspamd.conf
```

Be sure to pass the location of the configuration file to
pyrelay-rspamd when starting it.

Everything in the HEADERS section of the configuration file
is passed as an header to rspamd if you want to customize
the processing further. 
