from requests import auth
import requests

import config

auth_ = auth.HTTPBasicAuth(config.github_username, config.github_api_key)
headers = {'accept': 'application/vnd.github.black-cat-preview+json'}

repo_url = 'https://api.github.com/repos/gigwalk-corp/gigwalk_apps_platform_api'
labels_url = '{}/issues/{}/labels'.format(repo_url, 3294)

resp = requests.get(labels_url, auth=auth_, headers=headers)
print resp.content
