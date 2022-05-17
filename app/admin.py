from django.contrib import admin
from django.contrib.admin.models import LogEntry

from app.forms import GitModelForm
from app.models import Project, Git, Permissions


@admin.register(Project)
class ProjectAdminModel(admin.ModelAdmin):
    list_display = ('pk', 'project_path',)
    list_display_links = ('pk',)
    search_fields = ['project_path', ]
    ordering_fields = ('pk',)
    readonly_fields = ('owner',)

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.owner = request.user
        super().save_model(request, obj, form, change)


@admin.register(Git)
class GitAdminModel(admin.ModelAdmin):
    form = GitModelForm
    list_display = ('pk', 'username')


@admin.register(Permissions)
class PermissionsAdminModel(admin.ModelAdmin):
    list_display = ('pk', 'class_permission')



@admin.register(LogEntry)
class LogAdminModel(admin.ModelAdmin):
    list_display = ('user_id', 'object_repr', 'object_id', 'action_flag')
