import json

from requests import auth
import requests

import config
import pull_prs

auth_ = auth.HTTPBasicAuth(config.github_username, config.github_api_key)
headers = {'accept': 'application/vnd.github.black-cat-preview+json'}

repo_url = 'https://api.github.com/repos/gigwalk-corp/gigwalk_apps_platform_api'


'https://api.github.com/repos/freetheinterns/gigwalk_apps_platform_api/assignees{/user}'

# Get PRs

api = pull_prs.GitHubAPI()
all_prs = api.get('pulls?state=open')
for pr in all_prs:
  for assignee in pr['assignees']:
    print assignee['login']


# Get labels
# labels_url = '{}/issues/{}/labels'.format(repo_url, 3294)
# resp = requests.get(labels_url, auth=auth_, headers=headers)
# print resp.content
