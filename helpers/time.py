
"""Timestamps module."""

import pandas as pd
import locale


# set locale for timestamps (not the tz but words language, e.g. weekdays names)
locale.setlocale(locale.LC_TIME, locale.getlocale())

def now(tz: str = "Europe/Rome") -> pd.Timestamp:
    return pd.Timestamp.utcnow().tz_convert(tz)

def parse(t: str, tz: str = "Europe/Rome", format: str = "%Y-%m-%d %H:%M:%S", **kwargs) -> pd.Timestamp:
    return pd.to_datetime(t, format=format, **kwargs).tz_localize(tz)

def format(t: pd.Timestamp, format: str = "%Y-%m-%d %H:%M:%S") -> str:
    return t.strftime(format)
