from jiraintegration.util import week_ranges


def test_week_ranges():
    size = len(list(week_ranges(2019)))
    assert size > 0
