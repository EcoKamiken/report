#!/usr/bin/env python

from datetime import datetime
from datetime import timedelta

import report
import send

dt = datetime.now() - timedelta(hours=1)
from_addr = 'kamiken.nkjm@gmail.com'
to_addr = 'kamiken@sky.plala.or.jp,nakajima@kamiken.info'

sites = report.get_site_info()
for site in sites:
    t = report.low_power_alert(site['id'])
    if t:
        subject = '[Alert] {}'.format(site['name'])
        body = '''
        Low power alert

        {} ~ {}
        {} [kWh]
        '''.format(dt.strftime("%Y-%m-%d %H:00:00"), dt.strftime("%Y-%m-%d %H:59:59"), t)
        msg = send.create_message(from_addr, to_addr, subject, body)
        send.send(from_addr, to_addr.split(','), msg)