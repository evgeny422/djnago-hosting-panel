from django.urls import path

from app.views import ProjectListView, ProjectDetailView, RestartServe, MigrationApply, \
    StaticApply, ShowAccessLog, ShowErrorLog, GitBranch, GitPull, Shell, GunicornRestart

urlpatterns = [

    path('', ProjectListView.as_view(), name='task'),
    path('<int:pk>/', ProjectDetailView.as_view(), name='task_id'),
    path('shell/<int:pk>/', Shell.as_view(), name='shell'),
    path('restart/<int:pk>/', RestartServe.as_view(), name='restart'),
    path('restart_serve/<int:pk>/', GunicornRestart.as_view(), name='restart_serve'),
    path('pull/<int:pk>/', GitPull.as_view(), name='pull'),
    path('static/<int:pk>/', StaticApply.as_view(), name='static'),
    path('access_logs/<int:pk>/', ShowAccessLog.as_view(), name='access'),
    path('error_logs/<int:pk>/', ShowErrorLog.as_view(), name='error'),
    path('migrate/<int:pk>/', MigrationApply.as_view(), name='migrate'),
    path('<int:pk>/branch/', GitBranch.as_view(), name='branch'),

]
