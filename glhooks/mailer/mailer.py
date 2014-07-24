# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

import smtplib

from .compat import to_string


def _build_tls_mailer(host, port):
    mailer = smtplib.SMTP(host, port)
    mailer.ehlo()
    mailer.starttls()

    return mailer


class SmtpMailer(object):
    _MAILERS = {
        "tls": _build_tls_mailer,
        "ssl": smtplib.SMTP_SSL,
        "plain": smtplib.SMTP,
    }

    def __init__(self, user=None, password=None, host="", port=0, security="tls"):
        try:
            self._mailer = self._MAILERS[security]
        except KeyError:
            msg = "Incorrect value of security. Use one of the %s. Given: %s" % (
                "/".join(self._MAILERS.keys()),
                security,
            )
            raise ValueError(msg)

        self._user = user
        self._password = password
        self._host = host
        self._port = port

    def __call__(self, message):
        mailer = self._connect()
        try:
            return mailer.sendmail(message.sender, message.recipients, to_string(message))
        finally:
            mailer.quit()

    def _connect(self):
        mailer = self._mailer(self._host, self._port)
        mailer.ehlo()

        if self._user != None and self._password != None:
            raise Exception('WHY!!!!!!!!!!!!!!!!!!!!!!!!! %s' % self._password)
            mailer.login(self._user, self._password)

        return mailer


class GmailMailer(SmtpMailer):
    def __init__(self, user=None, password=None):
        super(GmailMailer, self).__init__(user, password, "smtp.gmail.com")
