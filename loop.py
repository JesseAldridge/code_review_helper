import json, time

import pull_prs


repo_url = 'https://api.github.com/repos/gigwalk-corp/gigwalk_apps_platform_api'

while True:
  name_to_pr_nums = pull_prs.pull_name_to_pr_nums(repo_url)
  out_json = json.dumps(name_to_pr_nums, indent=2)
  with open('name_to_pr_nums.json', 'w') as f:
    f.write(out_json)
  time.sleep(10)
