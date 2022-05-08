from django.contrib.auth.mixins import AccessMixin

from app.models import Permissions


class RequiredMixin:
    def get_access(self, key, request, *args, **kwargs):
        perm = Permissions.objects.prefetch_related('user').filter(user=self.request.user.id)
        for i in perm:
            if not i.class_permission == key:
                continue
            else:
                return super().dispatch(request, *args, **kwargs)
        return self.handle_no_permission()


class ShellRequiredMixin(AccessMixin, RequiredMixin):
    key = 1

    def dispatch(self, request, *args, **kwargs):
        return self.get_access(key=self.key, request=request, *args, **kwargs)


class ServeRequiredMixin(AccessMixin, RequiredMixin):
    key = 2

    def dispatch(self, request, *args, **kwargs):
        return self.get_access(key=self.key, request=request, *args, **kwargs)


class GitRequiredMixin(AccessMixin, RequiredMixin):
    key = 3

    def dispatch(self, request, *args, **kwargs):
        return self.get_access(key=self.key, request=request, *args, **kwargs)
