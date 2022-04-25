# Generated by Django 4.0.2 on 2022-03-01 12:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_database_logs_project_delete_task_logs_project_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='database',
            options={'verbose_name': 'DB', 'verbose_name_plural': 'DB'},
        ),
        migrations.AlterModelOptions(
            name='logs',
            options={'verbose_name': 'Логи', 'verbose_name_plural': 'Логи'},
        ),
        migrations.AlterModelOptions(
            name='project',
            options={'ordering': ['-id'], 'verbose_name': 'Репозиторий ', 'verbose_name_plural': 'Репозиторий'},
        ),
        migrations.RemoveField(
            model_name='database',
            name='project',
        ),
        migrations.RemoveField(
            model_name='logs',
            name='project',
        ),
        migrations.AddField(
            model_name='project',
            name='data_base',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.database'),
        ),
        migrations.AddField(
            model_name='project',
            name='logs',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.logs'),
        ),
    ]
