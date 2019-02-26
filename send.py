#!/usr/bin/env python

import os
import smtplib

from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

import report
from password.password import GMAIL_PASS

def create_message(from_addr, to_addr, subject, body, fig=False):
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = from_addr
    msg['To'] = to_addr

    text = MIMEText(body)
    msg.attach(text)

    if fig:
        img = open('figure.png', 'rb').read()
        image = MIMEImage(img, name=os.path.basename('figure.png'))
        msg.attach(image)

    return msg

def send(from_addr, to_addr, msg):
    smtp = smtplib.SMTP('smtp.gmail.com', 587)
    smtp.ehlo()
    smtp.starttls()
    smtp.ehlo()
    smtp.login(from_addr, GMAIL_PASS)
    smtp.sendmail(from_addr, to_addr, msg.as_string())
    smtp.close()

if __name__ == '__main__':
    sites = report.get_site_info()

    from_addr = 'kamiken.nkjm@gmail.com'
    to_addr = 'nakajima@kamiken.info'
    for site in sites:
        subject = 'daily report: {}'.format(site['name'])
        body = report.get_daily_report(site['id'])
        msg = create_message(from_addr, to_addr, subject, body, fig=True)
        send(from_addr, to_addr, msg)