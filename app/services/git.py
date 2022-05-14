import os
import re

from app.models import ProjectAbstract
from app.services.mixins import ShellConnection
from config.settings import bash_dir_path


class ProjectGit(ShellConnection):
    project: ProjectAbstract

    def __init__(self, project: ProjectAbstract):
        self.project = project

    def get_project(self) -> ProjectAbstract:
        return self.project

    def get_git_path(self):
        return self.get_project().get_git_path()

    def create_url(self, l, p):
        return f'https://{l}:{p}@gitlab.tspu.edu.ru/{l}/{self.return_repo()}.git'

    def return_repo(self):
        path = os.path.join(self.get_git_path(), 'config')
        with open(path) as file:
            lines = file.readlines()
            index_remote = lines.index('[remote "origin"]\n')
            return lines[index_remote + 1].strip().split('/')[-1].split('.')[0]

    def project_path(self) -> str:
        return self.get_project().get_path()

    def pull_private_rep(self, username, password):
        return self.script_apply(

            path=os.path.join(bash_dir_path, 'pull.sh'),
            param=self.project_path(),
            url=self.create_url(username, password)
        )

    def branch_apply(self, branch: str):
        return self.script_apply(path=os.path.join(bash_dir_path, 'branch.sh'), param=self.project_path(),
                                 branch=branch)
