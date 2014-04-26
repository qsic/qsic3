import os


def parse(envfile):
    """
    Return dict. One key, value pair for each
    `export ...` line within the envfile.
    Key is the environment variable name and
    value is the value.
    """
    envvars = {}
    with open(os.path.abspath(envfile)) as fp:
        for line in fp.readlines():
            if line[0:6] == 'export':
                line_list = line[6:].strip().split('=')
                envvars[line_list[0].strip()] = line_list[1].strip()

    return envvars
