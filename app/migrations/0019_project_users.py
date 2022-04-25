# Generated by Django 4.0.2 on 2022-04-19 11:38

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0018_project_env_path_project_git_path'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='users',
            field=models.ManyToManyField(related_name='developers', to=settings.AUTH_USER_MODEL),
        ),
    ]