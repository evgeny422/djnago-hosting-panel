import subprocess

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, DetailView

from app.forms import GitModelForm
from app.models import Project, Git
from app.services.django_service import ProjectManager
from app.services.git import ProjectGit
from app.services.nginx import ServeManager
from servises.exception_handling import base_view


class ProjectListView(ListView):
    """Список проектов"""

    model = Project
    template_name = 'projects/project_list.html'

    def get_queryset(self):
        return Project.objects.filter(users=self.request.user)


class ProjectDetailView(DetailView):
    """Проект по id"""

    model = Project
    template_name = 'projects/project_detail.html'


class RestartServe(View):
    """restart gunicorn"""

    @base_view
    def get(request, *args, **kwargs):
        try:
            project = ServeManager(Project.objects.get(id=kwargs['pk']))
            response = project.gunicorn_restart()
            return render(request, 'projects/shell.html', {'response': response, 'pk': kwargs['pk']})
            # return HttpResponse(response)
        except:
            raise Exception


class GunicornRestart(View):
    """Restart serve"""

    @base_view
    def post(self, request, *args, **kwargs):
        try:
            project = ServeManager(Project.objects.get(id=kwargs['pk']))
            key = request.POST.get('key')
            response = project.restart_serve(key=key)
            return render(request, 'projects/shell.html', {'response': response, 'pk': kwargs['pk']})
        except:
            raise ValueError('Invalid sudo key')


class ShowAccessLog(View):
    """Access logs"""

    @base_view
    def get(request, *args, **kwargs):
        project = ServeManager(Project.objects.get(id=kwargs['pk']))
        return HttpResponse(project.return_acces_log(), content_type='text/plain')


class ShowErrorLog(View):
    """Error logs"""

    @base_view
    def get(request, *args, **kwargs):
        project = ServeManager(Project.objects.get(id=kwargs['pk']))
        return HttpResponse(project.return_error_log(), content_type='text/plain')


class MigrationApply(View):
    """migrate"""

    @base_view
    def get(self, request, *args, **kwargs):
        try:
            project = ProjectManager(Project.objects.get(id=kwargs['pk']))
            response = project.migration_apply()
            return HttpResponse(response)
        except:
            raise Exception


class StaticApply(View):
    """collectstatic"""

    @base_view
    def get(self, request, *args, **kwargs):
        try:
            project = ProjectManager(Project.objects.get(id=kwargs['pk']))
            response = project.apply_collectstatic()
            return HttpResponse(response)
        except:
            raise Exception


class GitBranch(View):
    """change branch"""

    @base_view
    def get(self, request, *args, **kwargs):
        try:
            project = Project.objects.get(id=kwargs['pk'])
            pm = ProjectGit(project)
            branch = project.branch.get(id=request.GET.get('branch'))
            response = pm.branch_apply(branch)
            return render(request, 'projects/shell.html', {'response': response, 'pk': kwargs['pk']})
        except:
            raise Exception


class GitPull(View):
    """git pull"""

    @base_view
    def get(self, request, *args, **kwargs):
        project = Project.objects.get(id=kwargs['pk'])
        try:
            account = Git.objects.get(user=request.user)
            pm = ProjectGit(project)
            git = {
                'login': f'{account.get_username()}',
                'password': f'{account.get_password()}'
            }
            response = pm.pull_private_rep(username=git.get('login', None), password=git.get('password', None))
            return render(request, 'projects/shell.html', {'response': response, 'pk': kwargs['pk']})
        except:
            form = GitModelForm
            return render(request, 'git/git_create.html', {'form': form, 'pk': kwargs['pk']})

    @base_view
    def post(self, request, *args, **kwargs):
        checkout = request.POST.getlist('checkout')
        if '1' in checkout:
            """Save git-account and pull"""
            form = GitModelForm(request.POST)
            if form.is_valid():
                form = form.save(commit=False)
                form.user = request.user
                form.save()
            return redirect('pull', kwargs['pk'])

        """Pull without save git data"""
        project = Project.objects.get(id=kwargs['pk'])
        pm = ProjectGit(project)
        git = {
            'login': f'{request.POST.get("username", None)}',
            'password': f'{request.POST.get("password", None)}',
        }
        response = pm.pull_private_rep(
            username=git.get('login', None),
            password=git.get('password', None)
        )
        return render(request, 'projects/shell.html', {'response': response, 'pk': kwargs['pk']})


class Shell(View):
    """apply and get response by shell commands"""

    @base_view
    def get(self, request, *args, **kwargs):
        commands = request.GET.get('task')
        project = Project.objects.get(id=kwargs['pk'])

        if 'fatal ...' in commands:
            raise ValueError('Не допустимая команда')

        commands_apply = subprocess.check_output(f'cd {project.get_path()};{commands}', shell=True).decode()
        return HttpResponse(commands_apply)
