## jira-integration
Does something like this:

```
$ pipenv run python main.py --year 2019
Reading credentials from `config.json`

=== 2019-01-07 - 2019-01-13 ===
Key: AI-463, Resolved: 2019-01-11, Description: AI Tech Review #1, Status: Done
Key: AI-434, Resolved: 2019-01-10, Description: Return tag/ Id for transactions in S3 along with bv model scores , Status: Done

=== 2019-01-14 - 2019-01-20 ===
Key: AI-485, Resolved: 2019-01-17, Description: Investigate why these recurring transactions are not tagged, Status: Done
Key: AI-468, Resolved: 2019-01-14, Description: Fix dockerized ai-model-txcategorizer OutOfMemoryError issue, Status: Done
```

## Installation
```
git clone https://stash.moneylion.com/users/mauyong/repos/jira-integration
pipenv --python3.6 install
```

## Usage
```
pipenv run python main.py --year 2019 # Default value if not specified
pipenv run python main.py --year 2019 --async # Async option ¯\_(ツ)_/¯
```

You will be prompted for your email, token and JIRA server details. For API token, refer to https://confluence.atlassian.com/cloud/api-tokens-938839638.html
