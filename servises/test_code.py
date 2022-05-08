import os

import pexpect

from app.models import Project

path = os.path.join('/home/evgeny/project/.git', 'config')

with open(path) as file:
    lines = file.readlines()
    index_remote = lines.index('[remote "origin"]\n')
    print(lines[index_remote + 1].strip().split('/')[-1].split('.')[0])

