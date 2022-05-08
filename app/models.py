import os
import re
from abc import abstractmethod
from random import choice
from string import ascii_uppercase
from subprocess import PIPE, Popen
import cryptocode
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models

from myproject.settings import base_salt, bash_dir_path


class GitAbstract:
    @abstractmethod
    def get_username(self):
        pass

    @abstractmethod
    def get_password(self):
        pass


class ProjectAbstract:
    @abstractmethod
    def get_path(self):
        pass

    @abstractmethod
    def get_access_log_path(self):
        pass

    @abstractmethod
    def get_error_log_path(self):
        pass

    @abstractmethod
    def get_gunicorn_path(self):
        pass

    @abstractmethod
    def get_project_name(self):
        pass

    @abstractmethod
    def get_repo(self):
        pass

    @abstractmethod
    def get_git_path(self):
        pass

    @abstractmethod
    def get_env_path(self):
        pass


class Project(ProjectAbstract, models.Model):
    " Project\'s config "
    project_path = models.CharField(max_length=150)
    name = models.CharField('Название', max_length=300, blank=True)

    access_log_path = models.CharField('Access Logs', max_length=150, blank=True)
    error_log_path = models.CharField('Error Logs', max_length=150, blank=True)
    env_path = models.CharField('venv path', max_length=300, default=None, null=True, blank=True)
    git_path = models.CharField('.git path', max_length=300, default=None, null=True, blank=True)
    gunicorn_path = models.CharField('Gunicorn path', max_length=300, default=None, null=True, blank=True)

    branch_now = models.CharField('Branch', max_length=300, default='main')
    default_git = models.ForeignKey("Git", on_delete=models.SET_NULL, null=True, blank=True, related_name='default_git')

    users = models.ManyToManyField(User, related_name='developers', verbose_name='Developers')
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, default=1)

    class Meta:
        ordering = ['-id']
        verbose_name = 'Проект'
        verbose_name_plural = 'Проект'

    def clean(self):
        """Проверка на .git"""
        shell_response = Popen(f'bash {os.path.join(bash_dir_path, "git_status.sh")} {self.get_path()}', shell=True,
                               stdout=PIPE,
                               stderr=PIPE, bufsize=1, universal_newlines=True)
        stdout, stderr = shell_response.communicate()
        if stderr:
            raise ValidationError(f'Инициализируйте репозиторий. \n Error:{stderr}')

    def get_path(self):
        return self.project_path

    def get_env_path(self):
        if not self.env_path:
            return self.project_path

        return self.env_path

    def get_git_path(self):
        if not self.git_path:
            return os.path.join(f'{self.project_path}', '.git')

        return self.git_path

    def get_gunicorn_path(self):
        if not self.gunicorn_path:
            return self.project_path

        return self.gunicorn_path

    def get_access_log_path(self):
        return self.access_log_path

    def get_error_log_path(self):
        return self.error_log_path

    def get_project_name(self):
        return self.name

    def return_repo_branch(self):
        path = os.path.join(self.get_git_path(), 'config')
        with open(path) as f:
            lines = f.read()
            branch_in_lines = re.findall(r'\[branch (.*)\]', lines, flags=re.MULTILINE)
            branches = [re.sub('[ \"| \']', "", branch_in_lines[i]) for i in range(len(branch_in_lines))]
        return branches

    def __str__(self):
        return f'{self.project_path}'


class Git(GitAbstract, models.Model):
    "Git account info"
    username = models.CharField(max_length=100, null=True, blank=True)
    password = models.CharField(max_length=100, null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    salt = models.CharField(max_length=100, editable=False, default=None, null=True)

    class Meta:
        verbose_name = 'Git'
        verbose_name_plural = 'Git'

    def save(self, *args, **kwargs):
        """Пароль хранится в виде результата работы хеш-функции"""
        self.salt = (''.join(choice(ascii_uppercase) for i in range(12))) + base_salt
        self.password = cryptocode.encrypt(f'{self.password}', f'{self.salt}')
        return super(Git, self).save(*args, **kwargs)

    def get_username(self):
        return self.username

    def get_password(self):
        return cryptocode.decrypt(self.password, self.salt)

    def __str__(self):
        return '{}'.format(self.username)


class Permissions(models.Model):
    """Permissions class for users (developers) """
    CHOISES = (

        (1, "shell"),
        (2, "serve"),
        (3, "git"),
    )
    class_permission = models.PositiveSmallIntegerField(choices=CHOISES)
    user = models.ManyToManyField(User, related_name='permission')

    class Meta:
        verbose_name = 'Права доступа'
        verbose_name_plural = 'Права доступа'

    def __str__(self):
        return f'{self.class_permission}'

    def __repr__(self):
        return f'{self.class_permission}'
