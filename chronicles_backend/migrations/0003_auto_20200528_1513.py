# Generated by Django 3.0.5 on 2020-05-28 09:43

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chronicles_backend', '0002_auto_20200527_1719'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bugreport',
            name='creation',
            field=models.DateTimeField(default=datetime.datetime(2020, 5, 28, 15, 13, 7, 973212), verbose_name='Timestamp of bug report'),
        ),
        migrations.AlterField(
            model_name='bugreport',
            name='image',
            field=models.ImageField(null=True, upload_to='bugReportImages/'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='creation',
            field=models.DateTimeField(default=datetime.datetime(2020, 5, 28, 15, 13, 7, 974079), verbose_name='Timestamp of comment'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='image',
            field=models.ImageField(null=True, upload_to='commentImages/'),
        ),
        migrations.AlterField(
            model_name='project',
            name='creation',
            field=models.DateTimeField(default=datetime.datetime(2020, 5, 28, 15, 13, 7, 971838), verbose_name='Timestamp of project creation'),
        ),
    ]
