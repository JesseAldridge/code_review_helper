#!/usr/bin/python
import json

from requests import auth
import requests

import secrets


def pull_prs(repo_url):
  username = 'JesseAldridge'
  auth_ = auth.HTTPBasicAuth(username, secrets.github_api_key)


  def pull_reviewers(repo_url, pr_dict):
    reviewers_url = '{}/pulls/{}/requested_reviewers'.format(repo_url, pr_dict['number'])
    requested_reviewers = requests.get(reviewers_url, auth=auth_, headers=headers).json()
    names = [d['login'] for d in requested_reviewers]

    comments_url = pr_dict['_links']['comments']['href']
    comments = requests.get(comments_url, auth=auth_).json()

    line_comments_url = pr_dict['_links']['review_comments']['href']
    line_comments_resp = requests.get(line_comments_url, auth=auth_)
    line_comments = json.loads(line_comments_resp.content)

    return set([comment['user']['login'] for comment in comments + line_comments] + names)


  main_resp = requests.get('{}/pulls?state=open'.format(repo_url), auth=auth_)
  all_prs = json.loads(main_resp.content)

  headers = {'accept': 'application/vnd.github.black-cat-preview+json'}

  for pr in all_prs:
    if 'JesseAldridge' in pull_reviewers(repo_url, pr):
      print repo_url


if __name__ == '__main__':
    pull_prs('https://api.github.com/repos/gigwalk-corp/gigwalk_apps_platform_api')
