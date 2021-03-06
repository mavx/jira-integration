## jira-integration

[![Codefresh build status]( https://g.codefresh.io/api/badges/pipeline/mavx/default%2FJIRA-integration?branch=master&key=eyJhbGciOiJIUzI1NiJ9.NWNmNjAyOTg1NTFkNjBlMTNhY2U1NTli.Oha4MNwz3JEbcUT7jgue-awqAVtpY2pcSnXsVReS0vs&type=cf-1)]( https://g.codefresh.io/pipelines/JIRA-integration/builds?repoOwner=mavx&repoName=jira-integration&serviceName=mavx%2Fjira-integration&filter=trigger:build~Build;branch:master;pipeline:5cf60308f52abbac4891a980~JIRA-integration)

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
git clone https://github.com/mavx/jira-integration
pipenv --python 3.7 install
```

## Usage
```
pipenv run python main.py --year 2019 # Default value if not specified
pipenv run python main.py --year 2019 --async # Async option ¯\_(ツ)_/¯
```

## Developing
* Get pipenv `brew install pipenv`
* Run `build.sh` to apply code checks

You will be prompted for your email, token and JIRA server details. For API token, refer to https://confluence.atlassian.com/cloud/api-tokens-938839638.html
