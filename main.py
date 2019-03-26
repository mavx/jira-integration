from datetime import date, timedelta

import click
import crayons
from jira import JIRA
from jira.client import ResultList, Issue
from dateutil.parser import parse
import config

options = {'server': 'https://moneylion.atlassian.net'}
email, token = config.read()
if not (email and token):
    print("JIRA credentials need to be setup locally, you will be prompted for email and API token.")
    email = input("Email: ")
    token = input("Token: ")
    config.setup(email, token)
jira = JIRA(options, basic_auth=(email, token))


def all_mondays(year):
    d = date(year, 1, 1)
    d += timedelta(days=(7 - d.weekday()))
    while (d.year == year) and (d <= date.today()):
        yield d
        d += timedelta(days=7)


def week_ranges(year):
    for monday in all_mondays(year):
        yield monday, monday + timedelta(days=6)


def completed_issues(date_start, date_end):
    issues: ResultList = jira.search_issues(
        'project=AI AND status changed to Done during ("{}", "{}")'.format(date_start, date_end),
        maxResults=5, fields='summary,status,resolutiondate')

    return issues


def parse_date(date_str):
    return str(parse(date_str).date()) if date_str else None


@click.command()
@click.option('--year', default=date.today().year)
def main(year):
    for week_range in week_ranges(year):
        issues: ResultList = completed_issues(week_range[0], week_range[1])

        date_separator = "\n=== {} - {} ===".format(week_range[0], week_range[1])
        print(crayons.yellow(date_separator, bold=True))
        issue: Issue
        for issue in issues:
            resolution_date = parse_date(issue.fields.resolutiondate)
            print("Key: {}, Resolved: {}, Description: {}, Status: {}".format(issue.key, resolution_date,
                                                                              issue.fields.summary,
                                                                              issue.fields.status))


if __name__ == '__main__':
    main()
