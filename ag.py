#!/usr/bin/env python

import csv
import datetime
from pprint import pprint
from zoneinfo import ZoneInfo

import click


def get_tz_offset(dt):
    if isinstance(dt, datetime.date):
        dt = datetime.datetime.combine(dt, datetime.datetime.now().time())
    berlin_tz = ZoneInfo("Europe/Berlin")
    offset = int(berlin_tz.utcoffset(dt).seconds / 3600)
    return f"+0{offset}00"


def load_data(filename):
    with open(filename) as fp:
        reader = csv.DictReader(fp)
        for row in reader:
            yield row


def add_row(filename, new_row):
    with open(filename, "a") as fp:
        writer = csv.DictWriter(fp, fieldnames=new_row.keys(), lineterminator="\n")
        writer.writerow(new_row)


def gen_row(date, time):
    if not date:
        date = datetime.date.today()

    if not time:
        time = datetime.datetime.now()

    date_rolling = date
    if time.hour < 5:
        date_rolling = date - datetime.timedelta(days=1)

    return {
        "date": date.strftime("%Y-%m-%d"),
        "time": time.strftime("%H:%M"),
        "tz": get_tz_offset(date),
        "dayname": date.strftime("%a"),
        "date_rolling": date_rolling.strftime("%Y-%m-%d"),
    }


@click.command()
@click.option("--date", "-d", type=click.DateTime(formats=["%Y-%m-%d"]))
@click.option("--time", "-t", type=click.DateTime(formats=["%H:%M"]))
@click.option("--last", "-l", is_flag=True, default=False)
def main(date, time, last):
    filename = "augentropfen.data"

    if last:
        pprint(list(load_data(filename))[-1])
    else:
        add_row(filename, gen_row(date, time))


if __name__ == "__main__":
    main()
