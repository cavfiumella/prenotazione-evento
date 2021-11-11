
# module for timestamps


import pandas as pd


def now(tz: str = 'Europe/Rome') -> pd.Timestamp:
    return pd.Timestamp.utcnow().tz_convert(tz)


def parse(t: str, tz: str = 'Europe/Rome', format: str = '%Y-%m-%d %H:%M:%S', **kwargs) -> pd.Timestamp:
    return pd.to_datetime(t, format=format, **kwargs).tz_localize(tz)


def format(t: pd.Timestamp, format: str = '%Y-%m-%d %H:%M:%S') -> str:
    return t.strftime(format)
