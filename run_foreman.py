__author__ = 'paul'

from subprocess import call

try:
    call(["foreman", "start"])
except KeyboardInterrupt:
    print('foreman stopped.')