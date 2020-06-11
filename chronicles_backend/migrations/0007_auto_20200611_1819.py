# Generated by Django 3.0.5 on 2020-06-11 12:49

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chronicles_backend', '0006_auto_20200608_1535'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='chronicleuser',
            options={'ordering': ['enrNo']},
        ),
        migrations.AlterField(
            model_name='bugreport',
            name='creation',
            field=models.DateTimeField(default=datetime.datetime(2020, 6, 11, 18, 19, 12, 677177), verbose_name='Timestamp of bug report'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='creation',
            field=models.DateTimeField(default=datetime.datetime(2020, 6, 11, 18, 19, 12, 677677), verbose_name='Timestamp of comment'),
        ),
        migrations.AlterField(
            model_name='project',
            name='creation',
            field=models.DateTimeField(default=datetime.datetime(2020, 6, 11, 18, 19, 12, 675317), verbose_name='Timestamp of project creation'),
        ),
    ]
