
"""Timestamps module."""

import pandas as pd
import locale
from typing import Union


EN_IT = {
    "monday": "lunedì",
    "tuesday": "martedì",
    "wednesday": "mercoledì",
    "thursday": "giovedì",
    "friday": "venerdì",
    "saturday": "sabato",
    "sunday": "domenica",
    "january": "gennaio",
    "february": "febbario",
    "march": "marzo",
    "april": "aprile",
    "may": "maggio",
    "june": "giugno",
    "july": "luglio",
    "august": "august",
    "september": "settembre",
    "october": "ottobre",
    "november": "novembre",
    "december": "dicembre"
}


def set_locale(loc: str):
    locale.setlocale(locale.LC_TIME, loc)


def en_it(s: str) -> str:

    """Manually convert EN to IT locale."""

    s = s.split()
    new = []

    for word in s:
        if word.lower() in EN_IT:
            new += [EN_IT[word.lower()]]
        else:
            new += [word]

    return " ".join(new)


def now(tz: str = "Europe/Rome") -> pd.Timestamp:
    return pd.Timestamp.utcnow().tz_convert(tz)


def parse(t: str, tz: str = "Europe/Rome", format: str = "%Y-%m-%d %H:%M:%S", **kwargs) -> pd.Timestamp:
    return pd.to_datetime(t, format=format, **kwargs).tz_localize(tz)


def format(t: Union[pd.Timestamp, str], format: str = "%Y-%m-%d %H:%M:%S", loc: str = ("it_IT", "UTF-8")) -> str:

    if type(t) == str:
        t = parse(t)

    t = t.strftime(format)

    # current locale
    current_loc = locale.getlocale(locale.LC_TIME)
    if current_loc[0] == None:
        current_loc = locale.getlocale()

    if current_loc[0][:2] == "en" and loc[0][:2] == "it":
        t = en_it(t)

    return t
