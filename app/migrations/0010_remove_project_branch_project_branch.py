# Generated by Django 4.0.2 on 2022-04-02 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_remove_gitbranch_project_project_branch'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='branch',
        ),
        migrations.AddField(
            model_name='project',
            name='branch',
            field=models.ManyToManyField(to='app.GitBranch'),
        ),
    ]
