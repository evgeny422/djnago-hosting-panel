import subprocess

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.exceptions import PermissionDenied

from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, DetailView

from app.forms import GitModelForm, LoginUserForm, SudoEnterForm
from app.models import Project, Git, Permissions
from app.services.django_service import ProjectManager
from app.services.git import ProjectGit
from app.services.nginx import ServeManager
from permissions.developers_permissions import ServeRequiredMixin, GitRequiredMixin, ShellRequiredMixin
from services.exception_handling import base_view
from services.log_manage import LogWriter


class ProjectListView(LoginRequiredMixin, ListView):
    """Список проектов"""

    model = Project
    template_name = 'projects/project_list.html'

    def get_queryset(self):
        return Project.objects.prefetch_related('users').filter(users=self.request.user)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        user = self.request.user.id
        context['perm'] = Permissions.objects.prefetch_related('user').filter(user=user)
        context['sudo_form'] = SudoEnterForm
        return context


class ProjectDetailView(LoginRequiredMixin, DetailView):
    """Проект по id"""

    model = Project
    template_name = 'projects/project_detail.html'


class GunicornRestart(LoginRequiredMixin, ServeRequiredMixin, View):
    """Restart serve"""

    # @base_view
    def post(self, request, *args, **kwargs):
        project = ServeManager(Project.objects.get(id=kwargs['pk']))
        sudo_key = request.POST.get('sudo_key')
        form = SudoEnterForm(request.POST)
        if form.is_valid():
            response = project.restart_serve(key=sudo_key)
            LogWriter(request).write_log()
            return redirect('task')

        raise PermissionDenied


class ShowAccessLog(LoginRequiredMixin, ServeRequiredMixin, View):
    """Access logs"""

    @base_view
    def get(request, *args, **kwargs):
        project = ServeManager(Project.objects.get(id=kwargs['pk']))
        return HttpResponse(project.return_acces_log(), content_type='text/plain')


class ShowErrorLog(LoginRequiredMixin, ServeRequiredMixin, View):
    """Error logs"""

    @base_view
    def get(request, *args, **kwargs):
        project = ServeManager(Project.objects.get(id=kwargs['pk']))
        return HttpResponse(project.return_error_log(), content_type='text/plain')


class MigrationApply(LoginRequiredMixin, View):
    """migrate"""

    @base_view
    def get(self, request, *args, **kwargs):
        try:
            project = ProjectManager(Project.objects.get(id=kwargs['pk']))
            response = project.migration_apply()
            LogWriter(request).write_log()
            return HttpResponse(response)
        except:
            raise Http404('Object not exists')


class StaticApply(LoginRequiredMixin, View):
    """collectstatic"""

    @base_view
    def get(self, request, *args, **kwargs):
        try:
            pr = Project.objects.get(id=kwargs['pk'])
        except:
            raise Http404('Object not exists')
        project = ProjectManager(pr)
        response = project.apply_collectstatic()
        LogWriter(request).write_log()
        return HttpResponse(response)


class GitBranch(LoginRequiredMixin, GitRequiredMixin, View):
    """change branch"""

    @base_view
    def get(self, request, *args, **kwargs):
        try:
            project = Project.objects.get(id=kwargs['pk'])
        except:
            raise Http404('Object not exists')
        pm = ProjectGit(project)
        branch = request.GET.get('branch')
        response = pm.branch_apply(branch)
        project.branch_now = branch
        project.save()
        response += pm.get_url()

        LogWriter(request).write_log()
        return render(request, 'projects/shell.html', {'response': response, 'pk': kwargs['pk']})


class GitPull(LoginRequiredMixin, GitRequiredMixin, View):
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
            LogWriter(request).write_log()

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
        LogWriter(request).write_log()

        return HttpResponse(response)


class ShellView(View):

    @base_view
    def get(self, request, *args, **kwargs):
        return render(request, 'projects/shell.html', {'response': '', 'pk': kwargs['pk']})


class ShellApplyCommands(LoginRequiredMixin, ShellRequiredMixin, View):
    """Ajax apply shell commands"""

    @base_view
    def get(self, request, *args, **kwargs):
        commands = request.GET.get('task')
        project = Project.objects.get(id=kwargs['pk'])
        forbidden_commands = {'fatal', }

        if forbidden_commands.intersection(set(commands.split(';')[:-1])):
            raise ValueError('Не допустимая команда')

        commands_apply = subprocess.check_output(f'cd {project.get_path()};{commands}', shell=True).decode()
        LogWriter(request).write_log()
        return HttpResponse(commands_apply)


class UserLogIn(LoginView):
    form_class = LoginUserForm
    template_name = 'login.html'
