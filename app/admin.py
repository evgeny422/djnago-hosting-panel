from django.contrib import admin
from django.contrib.admin.models import LogEntry

from app.forms import GitModelForm
from app.models import Project, Git, GitBranch


@admin.register(Project)
class ProjectAdminModel(admin.ModelAdmin):
    list_display = ('pk', 'project_path',)
    list_display_links = ('pk',)
    search_fields = ['project_path', ]
    ordering_fields = ('pk',)


@admin.register(Git)
class GitAdminModel(admin.ModelAdmin):
    form = GitModelForm
    list_display = ('pk', 'username')


@admin.register(GitBranch)
class BranchAdminModel(admin.ModelAdmin):
    list_display = ('pk', 'title')


@admin.register(LogEntry)
class LogAdminModel(admin.ModelAdmin):
    list_display = ('user_id', 'object_repr', 'object_id', 'action_flag')
