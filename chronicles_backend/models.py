from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime


class ChronicleUser(AbstractUser):
    enrNo = models.IntegerField(default=0)
    isAdmin = models.BooleanField(default=False)

    def __str__(self):
        return self.get_username()


class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    creator = models.ForeignKey(ChronicleUser, null=True, on_delete=models.SET_NULL, related_name='created_projects')
    team = models.ManyToManyField(ChronicleUser, related_name='projects')
    creation = models.DateTimeField(default=datetime.now(), verbose_name='Timestamp of project creation')
    image = models.ImageField(upload_to='projectImages/', default='projectImages/default.png')
    slug = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class BugReport(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    reporter = models.ForeignKey(ChronicleUser, null=True, on_delete=models.SET_NULL, related_name='reported_bugs')
    heading = models.CharField(max_length=500)
    description = models.CharField(max_length=2000)
    person_in_charge = models.ForeignKey(ChronicleUser, null=True, on_delete=models.SET_NULL,
                                         related_name='bugs_assigned')
    creation = models.DateTimeField(default=datetime.now(), verbose_name='Timestamp of bug report')
    status = models.BooleanField(default=False)
    tagsHash = models.IntegerField(default=0)
    image = models.ImageField(upload_to='bugReportImages/', null=True)

    class Meta:
        ordering = ['status', 'creation']

    def __str__(self):
        return f"{self.project}::{self.heading}"


class Comment(models.Model):
    report = models.ForeignKey(BugReport, on_delete=models.CASCADE)
    creation = models.DateTimeField(default=datetime.now(), verbose_name='Timestamp of comment')
    commenter = models.ForeignKey(ChronicleUser, null=True, on_delete=models.SET_NULL)
    body = models.CharField(max_length=1000)
    image = models.ImageField(upload_to='commentImages/', null=True)

    class Meta:
        ordering = ['-creation']

    def __str__(self):
        return f"{self.report.project}::{self.report}::{self.body}"


class Image(models.Model):
    randIdentifier = models.CharField(max_length=100)
    url = models.ImageField(upload_to='imageWarehouse/')
