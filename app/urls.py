from django.urls import path

from app.views import ProjectListView, ProjectDetailView, MigrationApply, \
    StaticApply, ShowAccessLog, ShowErrorLog, GitBranch, GitPull, ShellApplyCommands, GunicornRestart, UserLogIn, \
    ShellView

urlpatterns = [

    path('', ProjectListView.as_view(), name='task'),
    path('<int:pk>/', ProjectDetailView.as_view(), name='task_id'),
    path('login/', UserLogIn.as_view(), name="login"),
    path('shell_console/<int:pk>/', ShellView.as_view(), name='shell_commands'),
    path('shell_commands/<int:pk>/', ShellApplyCommands.as_view(), name='shell'),
    path('restart_serve/<int:pk>/', GunicornRestart.as_view(), name='restart_serve'),
    path('pull/<int:pk>/', GitPull.as_view(), name='pull'),
    path('static_apply/<int:pk>/', StaticApply.as_view(), name='static'),
    path('access_logs/<int:pk>/', ShowAccessLog.as_view(), name='access'),
    path('error_logs/<int:pk>/', ShowErrorLog.as_view(), name='error'),
    path('migrate/<int:pk>/', MigrationApply.as_view(), name='migrate'),
    path('<int:pk>/branch/', GitBranch.as_view(), name='branch'),

]
