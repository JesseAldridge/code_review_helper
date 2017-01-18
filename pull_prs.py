#!/usr/bin/python
import json, time

from requests import auth
import requests

import config


class GitHubAPI:
  def __init__(self):
    self.auth = auth.HTTPBasicAuth(config.github_username, config.github_api_key)

  def get(self, url):
    headers = {'accept': 'application/vnd.github.black-cat-preview+json'}
    repo_url = 'https://api.github.com/repos/gigwalk-corp/gigwalk_apps_platform_api'

    if not url.startswith('http'):
      url = '/'.join((repo_url, url))

    for _ in range(10):
      resp = requests.get(url, auth=self.auth, headers=headers)
      if int(resp.headers.get('x-ratelimit-remaining', 100)) < 10:
        reset_time = resp.headers['X-RateLimit-Reset']
        print 'rate limit exceeded, reset_time:', reset_time, 'curr time:', time.time()
        time.sleep(120)
        continue
      break

    print 'xrate-limit-remaining:', resp.headers.get('x-ratelimit-remaining')
    return resp.json()


def pull_name_to_pr_nums(repo_url, testing=False):
  def pull_reviewers(pr_dict):
    reviewers_url = 'pulls/{}/requested_reviewers'.format(pr_dict['number'])

    requested_reviewers = api.get(reviewers_url)
    names = [d['login'] for d in requested_reviewers]

    comments_url = pr_dict['_links']['comments']['href']
    comments = api.get(comments_url)

    line_comments_url = pr_dict['_links']['review_comments']['href']
    line_comments = api.get(line_comments_url)

    pr_creator = pr_dict['user']['login']
    try:
      names += [comment['user']['login'] for comment in comments + line_comments]
    except Exception as e:
      print 'Exception!'
      print 'comments:', comments
      print 'line_comments:', line_comments
      print 'names:', names
      raise
    return set(names) - set([pr_creator])

  api = GitHubAPI()
  all_prs = api.get('pulls?state=open')

  name_to_pr_nums = {}
  pr_num_to_labels = {}
  prs = all_prs[::-1]
  for pr_dict in prs[:2] if testing else prs:
    print 'pulling info for:', pr_dict['url']

    '''
    labels json:
    [{"id":280513186,
      "url":"https://api.github.com/repos/gigwalk-corp/gigwalk_apps_platform_api/labels/needs-work",
      "name":"needs-work","color":"006b75","default":false},
      {"id":324952392,
       "url":"https://api.github.com/repos/gigwalk-corp/gigwalk_apps_platform_api/labels/p1-reviewlist-dev",
       "name":"p1-reviewlist-dev","color":"d4c5f9","default":false}]
    '''
    labels_url = '{}/issues/{}/labels'.format(repo_url, pr_dict['number'])
    pr_num_to_labels[pr_dict['number']] = []
    for label_dict in api.get(labels_url):
      pr_num_to_labels[pr_dict['number']].append(label_dict)

    reviewer_names = pull_reviewers(pr_dict) or ['(No Reviewers Yet)']
    for reviewer_name in reviewer_names:
      name_to_pr_nums.setdefault(reviewer_name, [])
      name_to_pr_nums[reviewer_name].append(pr_dict['number'])

  return name_to_pr_nums, pr_num_to_labels


if __name__ == '__main__':
  repo_url = 'https://api.github.com/repos/gigwalk-corp/gigwalk_apps_platform_api'
  name_to_pr_nums, pr_num_to_labels = pull_name_to_pr_nums(repo_url, testing=True)
  print 'name_to_pr_nums:', name_to_pr_nums
  print 'pr_num_to_labels:', pr_num_to_labels

  assert len(name_to_pr_nums) > 0
  assert isinstance(name_to_pr_nums['JesseAldridge'][0], int)
  assert len(pr_num_to_labels) > 0
  assert isinstance(pr_num_to_labels.items()[0][1][0]['name'], unicode)
