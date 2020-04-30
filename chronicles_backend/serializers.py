from rest_framework import serializers
from chronicles_backend.models import *


class ProjectSerializer(serializers.ModelSerializer):
    """Serializes Project list"""
    class Meta:
        model = Project
        fields = ['id', 'name', 'description']


# feed serializers needed


class UserSerializerSmall(serializers.ModelSerializer):
    """Short user serializer for foreign keys"""
    class Meta:
        model = ChronicleUser
        fields = ['id', 'name']


class ProjectSerializerAdmin(serializers.ModelSerializer):
    """Project serializer for admin"""
    teamMembers = UserSerializerSmall(source='team', many=True)

    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'creator', 'teamMembers', 'creation']


class UserSerializer(serializers.ModelSerializer):
    """User Serializer"""

    projectList = ProjectSerializer(source='projects', many=True)
    noOfIssues = BugReport.objects.filter(pk='id').count()

    class Meta:
        model = ChronicleUser
        fields = ['id', 'name', 'projectList', 'isAdmin', 'noOfIssues']


class BugReportSerializer(serializers.ModelSerializer):
    """Serializer for bug reports"""

    class Meta:
        model = BugReport
        fields = ['reporter', 'heading', 'description', 'creation', 'status']


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for Comments"""

    class Meta:
        model = Comment
        fields = ['commenter', 'creation', 'body']
