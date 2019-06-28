from datetime import date, timedelta

from dateutil.parser import parse


def all_mondays(year):
    d = date(year, 1, 1)
    d += timedelta(days=(7 - d.weekday()))
    while (d.year == year) and (d <= date.today()):
        yield d
        d += timedelta(days=7)


def week_ranges(year):
    for monday in all_mondays(year):
        yield monday, monday + timedelta(days=6)


def parse_date(date_str):
    return str(parse(date_str).date()) if date_str else None
