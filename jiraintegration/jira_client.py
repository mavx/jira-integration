import asyncio

import crayons
from jira import JIRA, Issue
from jira.client import ResultList

from jiraintegration import config
from jiraintegration.util import week_ranges, parse_date


class JiraClient:
    def __init__(self):
        email, token, server = config.read()
        if not (email and token and server):
            print(
                "JIRA credentials need to be setup locally, "
                "you will be prompted for email and API token."
            )
            server = input("JIRA URL (e.g. https://moneylion.atlassian.net): ")
            email = input("Email: ")
            token = input("Token (from https://id.atlassian.com/manage/api-tokens): ")
            config.setup(email, token, server)
        options = {"server": server}
        self.jira = JIRA(options, basic_auth=(email, token))

    def completed_issues(self, project, date_start, date_end):
        issues: ResultList = self.jira.search_issues(
            'project={} AND status changed to Done during ("{}", "{}")'.format(
                project, date_start, date_end
            ),
            maxResults=5,
            fields="summary,status,resolutiondate",
        )

        return issues

    def completed_issues_json(self, project, date_start, date_end):
        issues: ResultList = self.jira.search_issues(
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

    def print_issues(self, project, year):
        for week_range in week_ranges(year):
            issues: ResultList = self.completed_issues(
                project, week_range[0], week_range[1]
            )

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

    async def print_issues_async(self, project, year, executor):
        loop = asyncio.get_event_loop()
        tasks = [
            loop.run_in_executor(
                executor, self.completed_issues_json, project, week[0], week[1]
            )
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
