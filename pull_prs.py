#!/usr/bin/python
import json

from requests import auth
import requests

import config


def pull_name_to_pr_nums(repo_url):
  auth_ = auth.HTTPBasicAuth(config.github_username, config.github_api_key)

  def pull_reviewers(pr_dict):
    reviewers_url = '{}/pulls/{}/requested_reviewers'.format(repo_url, pr_dict['number'])
    headers = {'accept': 'application/vnd.github.black-cat-preview+json'}
    print 'pulling reviewers for:', reviewers_url
    requested_reviewers = requests.get(reviewers_url, auth=auth_, headers=headers).json()
    names = [d['login'] for d in requested_reviewers]

    comments_url = pr_dict['_links']['comments']['href']
    comments = requests.get(comments_url, auth=auth_).json()

    line_comments_url = pr_dict['_links']['review_comments']['href']
    line_comments_resp = requests.get(line_comments_url, auth=auth_)
    line_comments = json.loads(line_comments_resp.content)

    pr_creator = pr_dict['user']['login']

    names += [comment['user']['login'] for comment in comments + line_comments]

    return set(names) - set([pr_creator])


  main_resp = requests.get('{}/pulls?state=open'.format(repo_url), auth=auth_)
  all_prs = json.loads(main_resp.content)

  name_to_pr_nums = {}
  for pr_dict in all_prs[::-1]:
    for reviewer_name in pull_reviewers(pr_dict):
      name_to_pr_nums.setdefault(reviewer_name, [])
      name_to_pr_nums[reviewer_name].append(pr_dict['number'])

  return name_to_pr_nums


if __name__ == '__main__':
  repo_url = 'https://api.github.com/repos/gigwalk-corp/gigwalk_apps_platform_api'
  name_to_pr_nums = pull_name_to_pr_nums(repo_url)
  print name_to_pr_nums

  assert len(name_to_pr_nums) > 0
  assert isinstance(name_to_pr_nums['JesseAldridge'][0], int)
