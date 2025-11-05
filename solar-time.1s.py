#!/usr/bin/env python
# -*- mode: python; coding: utf-8 -*-
#
# <bitbar.title>Apparent Solar Time</bitbar.title>
# <bitbar.version>v1.5</bitbar.version>
# <bitbar.author>Alexandre André</bitbar.author>
# <bitbar.author.github>XanderLeaDaren</bitbar.author.github>
# <bitbar.desc>Displays the apparent solar time.</bitbar.desc>
# <bitbar.image>https://github.com/XanderLeaDaren/bitbar-solar-time/blob/master/bitbar_solar-time.jpg?raw=true</bitbar.image>
# <bitbar.dependencies>python</bitbar.dependencies>
# <bitbar.abouturl>https://github.com/XanderLeaDaren/bitbar-solar-time</bitbar.abouturl>
#
# <bitbar.var>string(VAR_PREFIX="☀️ "): Text to display to the left of the time.</bitbar.var>
# <bitbar.var>boolean(VAR_DISPLAY_SECONDS=true): Display the time with seconds.</bitbar.var>

import datetime
from math import sin,pi
import os
import time
import json
import urllib

def get_longitude():
    url = 'http://ip-api.com/json/?fields=lon'
    response = urllib.urlopen(url)
    data = response.read()
    text = data.decode ('utf-8')
    coordinates = json.loads(text)
    location = coordinates["lon"]
    return location

def get_position():
    return float(get_longitude()) / 360 * 24 * 60

def get_eq_time(day):
    return 7.655 * sin(2 * (day - 4) * pi / 365.25) + 9.873 * sin(4 * (day - 172) * pi / 365.25)

def get_sun_time(today, pos, eq_time, tz):
    return today - datetime.timedelta(minutes = -pos + eq_time, seconds = -tz)

def print_information():
    today = datetime.datetime.now()
    day = today.timetuple().tm_yday
    tz = time.altzone
    pos = get_position()
    eq_time = get_eq_time(day)
    sun_time = get_sun_time(today, pos, eq_time, tz)

    if os.environ.get('VAR_DISPLAY_SECONDS') == 'false':
        time_fmt = '%H:%M'
    else:
        time_fmt = '%H:%M:%S'
    prefix = os.environ.get('VAR_PREFIX')
    if prefix is None:
        prefix = "☀️ "
    print prefix + sun_time.strftime(time_fmt)
    print "---"
    print "Time Zone Offset: " + str(tz / 3600) + " h"
    print "Position Offset: %.3f" % pos + " min"
    print "Equation of Time: %.3f" % -eq_time + " min"

if __name__ == "__main__":
    print_information()
