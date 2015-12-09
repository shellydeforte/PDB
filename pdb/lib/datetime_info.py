# -*- coding: utf-8 -*-
"""Create ISO 8601 compliant date and time stamps."""
from __future__ import (
    absolute_import, division, print_function, unicode_literals)

import pytz
import re

from datetime import datetime


class RE(object):
    datetime_stamp_pattern = """
        ^                   # Anchor to the beginning of string.
        # Named references.
        (?P<year>\d{4})
        (?P<month>\d{2})
        (?P<day>\d{2})
        T                   # Delimiter (Begin time.)
        (?P<hour>\d{2})
        (?P<minute>\d{2})
        (?P<second>\d{2})
        Z                   # Indicate UTC TZ.
    """
    datetime_pat = re.compile(datetime_stamp_pattern, re.VERBOSE)


def now_utc():
    return datetime.utcnow().strftime("%Y%m%dT%H%M%S" + "Z")


def create_dt_obj(time_stamp):
    dt = RE.datetime_pat.search(time_stamp)
    assert dt
    dt_obj = datetime(
        int(dt.group('year')),
        int(dt.group('month')),
        int(dt.group('day')),
        hour=int(dt.group('hour')),
        minute=int(dt.group('minute')),
        second=int(dt.group('second')),
        tzinfo=pytz.UTC
    )
    return dt_obj
