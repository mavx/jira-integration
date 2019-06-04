import asyncio
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import date, timedelta

import click
import crayons
from dateutil.parser import parse
from jira import JIRA
from jira.client import ResultList, Issue

import config

email, token, server = config.read()
if not (email and token and server):
    print(
        "JIRA credentials need to be setup locally, you will be prompted for email and API token."
    )
    server = input("JIRA URL (e.g. https://moneylion.atlassian.net): ")
    email = input("Email: ")
    token = input("Token (from https://id.atlassian.com/manage/api-tokens): ")
    config.setup(email, token, server)
options = {"server": server}
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


def completed_issues(project, date_start, date_end):
    issues: ResultList = jira.search_issues(
        'project={} AND status changed to Done during ("{}", "{}")'.format(
            project, date_start, date_end
        ),
        maxResults=5,
        fields="summary,status,resolutiondate",
    )

    return issues


def completed_issues_json(project, date_start, date_end):
    issues: ResultList = jira.search_issues(
        'project={} AND status changed to Done during ("{}", "{}")'.format(
            project, date_start, date_end
        ),
        maxResults=5,
        fields="summary,status,resolutiondate",
    )

    return {
        "date_start": str(date_start),
        "date_range": (date_start, date_end),
        "issues": issues,
    }


def parse_date(date_str):
    return str(parse(date_str).date()) if date_str else None


def print_issues(project, year):
    for week_range in week_ranges(year):
        issues: ResultList = completed_issues(project, week_range[0], week_range[1])

        date_separator = "\n=== {} - {} ===".format(week_range[0], week_range[1])
        print(crayons.yellow(date_separator, bold=True))
        issue: Issue
        for issue in issues:
            resolution_date = parse_date(issue.fields.resolutiondate)
            print(
                "Key: {}, Resolved: {}, Description: {}, Status: {}".format(
                    issue.key,
                    resolution_date,
                    issue.fields.summary,
                    issue.fields.status,
                )
            )


async def print_issues_async(project, year, executor):
    loop = asyncio.get_event_loop()
    tasks = [
        loop.run_in_executor(executor, completed_issues_json, project, week[0], week[1])
        for week in week_ranges(year)
    ]
    completed, pending = await asyncio.wait(tasks)
    results_gen = [t.result() for t in completed]
    results_dict = {res["date_start"]: res for res in results_gen}

    for res in sorted(results_dict.items()):
        issue_dict = res[1]
        date_range = issue_dict["date_range"]
        issues: ResultList = issue_dict["issues"]

        date_separator = "\n=== {} - {} ===".format(date_range[0], date_range[1])
        print(crayons.yellow(date_separator, bold=True))

        issue: Issue
        for issue in issues:
            resolution_date = parse_date(issue.fields.resolutiondate)
            print(
                "Key: {}, Resolved: {}, Description: {}, Status: {}".format(
                    issue.key,
                    resolution_date,
                    issue.fields.summary,
                    issue.fields.status,
                )
            )


@click.command()
@click.option("--project", default="AI", help="JIRA project key, e.g. AI, DE")
@click.option("--year", default=date.today().year, help="Query issues in this year")
@click.option("--async/--no-async", "_async", default=False)
def main(project: str, year, _async=False):
    start = time.time()

    if _async:
        executor = ThreadPoolExecutor()
        asyncio.run(print_issues_async(project.upper(), year, executor))
    else:
        print_issues(project.upper(), year)
        print("OLA!")

    duration = time.time() - start
    print(crayons.green("\nElapsed: {:.2f}s".format(duration), bold=True))
    print(" SO NOT COMPLIANT" )
    print( " Trigger another build "   )


def weird_func(kasdf=True):
    print(kasdf)


if __name__ == "__main__":
    main()
