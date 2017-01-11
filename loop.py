import json, time

import pull_prs, config


repo_url = 'https://api.github.com/repos/gigwalk-corp/gigwalk_apps_platform_api'

while True:
  name_to_pr_nums, pr_num_to_labels = pull_prs.pull_name_to_pr_nums(repo_url)
  out_json = json.dumps({
    'name_to_pr_nums': name_to_pr_nums,
    'pr_num_to_labels': pr_num_to_labels
  }, indent=2)
  with open(config.report_path, 'w') as f:
    f.write(out_json)
  time.sleep(10)
