import sys, json, os
from datetime import datetime

import flask

import config


app = flask.Flask(__name__)
port = int(sys.argv[1]) if len(sys.argv) == 2 else 80


@app.route('/')
def index():
  mod_time = os.path.getmtime(config.report_path)
  last_mod_dt = datetime.fromtimestamp(mod_time)

  with open(config.report_path) as f:
    main_json = f.read()
  main_dict = json.loads(main_json)
  name_to_pr_nums = main_dict['name_to_pr_nums']
  pr_num_to_labels = main_dict['pr_num_to_labels']

  return flask.render_template('index.html', name_to_pr_nums=name_to_pr_nums,
                               pr_num_to_labels=pr_num_to_labels, last_mod_dt=last_mod_dt)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=(port != 80))

