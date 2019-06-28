import asyncio
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import date

import click
import crayons

from src.jira_client import JiraClient


@click.command()
@click.option("--project", default="AI", help="JIRA project key, e.g. AI, DE")
@click.option("--year", default=date.today().year, help="Query issues in this year")
@click.option("--async/--no-async", "_async", default=False)
def main(project: str, year, _async=False):
    start = time.time()
    jira = JiraClient()

    if _async:
        executor = ThreadPoolExecutor()
        asyncio.run(jira.print_issues_async(project.upper(), year, executor))
    else:
        jira.print_issues(project.upper(), year)

    duration = time.time() - start
    print(crayons.green("\nElapsed: {:.2f}s".format(duration), bold=True))


if __name__ == "__main__":
    main()
