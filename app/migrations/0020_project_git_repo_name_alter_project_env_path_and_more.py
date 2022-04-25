# Generated by Django 4.0.2 on 2022-04-19 11:42

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0019_project_users'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='git_repo_name',
            field=models.CharField(blank=True, max_length=300, verbose_name='Название репозитория'),
        ),
        migrations.AlterField(
            model_name='project',
            name='env_path',
            field=models.CharField(blank=True, default=None, max_length=300, null=True, verbose_name='venv path'),
        ),
        migrations.AlterField(
            model_name='project',
            name='git_path',
            field=models.CharField(blank=True, default=None, max_length=300, null=True, verbose_name='.git path'),
        ),
        migrations.AlterField(
            model_name='project',
            name='users',
            field=models.ManyToManyField(related_name='developers', to=settings.AUTH_USER_MODEL, verbose_name='Developers'),
        ),
    ]
