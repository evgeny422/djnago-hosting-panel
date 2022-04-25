# Generated by Django 4.0.2 on 2022-02-24 05:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='title',
        ),
        migrations.AddField(
            model_name='task',
            name='path',
            field=models.CharField(default=1, max_length=150, verbose_name='Путь'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='task',
            name='description',
            field=models.TextField(blank=True, max_length=300, verbose_name='Описани'),
        ),
    ]