__author__ = 'paul'

import os
from subprocess import call

from local.parse_env_file import parse

envvars = parse('local/enter_env.sh')

for k, v in envvars.items():
    os.environ.update(envvars)

try:
    call(["foreman", "start"])
except KeyboardInterrupt:
    print('\nforeman stopped.')