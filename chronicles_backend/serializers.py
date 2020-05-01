from rest_framework import serializers
from chronicles_backend.models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChronicleUser
        fields = ['id', 'username', 'first_name', 'last_name']


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'creator', 'team', 'creation']
        read_only_fields = ['creation']


class BugReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = BugReport
        fields = ['id', 'project', 'reporter', 'heading', 'description', 'person_in_charge', 'creation', 'status']
        read_only_fields = ['creation']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'report', 'creation', 'commenter', 'body']
        read_only_fields = ['creation']
