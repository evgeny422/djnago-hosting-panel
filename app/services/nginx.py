import os

import pexpect

from app.models import ProjectAbstract
from app.services.mixins import ShellConnection
from config.settings import bash_dir_path


class LogsManager:
    def __init__(self, log_path):
        self._log_path = log_path

    def return_massage(self):
        try:
            f = open(self._log_path, 'r')
        except:
            raise ValueError('File not readable ')
        file_content = f.read()
        f.close()
        return file_content


class ServeManager(ShellConnection):

    def __init__(self, project: ProjectAbstract):
        self.project = project

    def get_project(self) -> ProjectAbstract:
        return self.project

    def return_acces_log(self):
        log = LogsManager(log_path=self.get_project().get_access_log_path())
        return log.return_massage()

    def return_error_log(self):
        log = LogsManager(log_path=self.get_project().get_error_log_path())
        return log.return_massage()

    def restart_serve(self, key=None):
        try:
            res = pexpect.spawn(
                command=f'bash {os.path.join(bash_dir_path, "gunicorn_restart.sh")} {self.get_project().get_gunicorn_path}')
            res.expect(['[sudo]'])
            res.sendline(f'{key}')
            res.expect(pexpect.EOF)
            res.close()
        except:
            raise pexpect.exceptions.ExceptionPexpect

        return 'Serve was restarted'
