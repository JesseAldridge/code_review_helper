#!/usr/bin/python
import json, time, traceback

from requests import auth
import requests

import config


class GitHubAPI:
  def __init__(self):
    self.auth = auth.HTTPBasicAuth(config.github_username, config.github_api_key)

  def get(self, url):
    print 'getting:', url

    headers = {'accept': 'application/vnd.github.black-cat-preview+json'}
    repo_url = 'https://api.github.com/repos/gigwalk-corp/gigwalk_apps_platform_api'

    if not url.startswith('http'):
      url = '/'.join((repo_url, url))

    for _ in range(10):
      time.sleep(1)
      try:
        print 'getting:', url
        resp = requests.get(url, auth=self.auth, headers=headers, timeout=10)
      except Exception as e:
        print (u'exception: {}; {}'.format(type(e).__name__, e.message)).encode('utf8')
        traceback.print_exc()
        continue
      if int(resp.headers.get('x-ratelimit-remaining', 100)) < 10:
        reset_time = resp.headers['X-RateLimit-Reset']
        print 'rate limit exceeded, reset_time:', reset_time, 'curr time:', time.time()
        time.sleep(240)
        continue
      break

    print 'xrate-limit-remaining:', resp.headers.get('x-ratelimit-remaining')
    return resp.json()

api = GitHubAPI()


def pull_name_to_pr_nums(repo_url, testing=False):
  print 'pulling all prs'
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

    reviewer_names = ({d['login'] for d in pr_dict['assignees']} - {pr_dict['user']['login']} or
                      {'(No Reviewers Yet)'})
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
