__author__ = 'paul'

import os
from subprocess import call


try:
    call(["foreman", "start"])
except KeyboardInterrupt:
    print('\nforeman stopped.')