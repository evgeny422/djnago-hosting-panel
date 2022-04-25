import os

from app.models import Project
from app.services.mixins import ShellConnection
from myproject.settings import bash_dir_path


class ProjectManager(ShellConnection):

    def __init__(self, project: Project):
        self.project = project

    def get_project(self) -> Project:
        return self.project

    def migration_apply(self):
        """./manage.py migrate"""

        return self.script_apply(path=os.path.join(bash_dir_path, 'migration_script.sh'),
                                 param=self.get_project().get_env_path())

    def apply_collectstatic(self):
        """./manage.py collectstatic"""

        return self.script_apply(path=os.path.join(bash_dir_path, 'static_apply.sh'),
                                 param=self.get_project().get_env_path())
