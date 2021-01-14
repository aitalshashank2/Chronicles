# Generated by Django 3.0.7 on 2021-01-13 16:54

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chronicles_backend', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bugreport',
            name='creation',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name='Timestamp of bug report'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='creation',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name='Timestamp of comment'),
        ),
        migrations.AlterField(
            model_name='project',
            name='creation',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name='Timestamp of project creation'),
        ),
    ]