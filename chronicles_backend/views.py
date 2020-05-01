from django.shortcuts import render
from rest_framework import viewsets
from .models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ChronicleUser.objects.all()
    serializer_class = UserSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class BugReportViewSet(viewsets.ModelViewSet):
    queryset = BugReport.objects.all()
    serializer_class = BugReportSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class MembersOfProject(APIView):

    def get(self, request, pk, format=None):
        serializer = UserSerializer(Project.objects.get(pk=pk).team.all(), many=True)
        return Response(serializer.data)


class BugsOfProject(APIView):

    def get(self, request, pk, format=None):
        serializer = BugReportSerializer(Project.objects.get(pk=pk).bugreport_set.all(), many=True)
        return Response(serializer.data)


class CommentsOnBugs(APIView):

    def get(self, request, pk, format=None):
        serializer = CommentSerializer(BugReport.objects.get(pk=pk).comment_set.all(), many=True)
        return Response(serializer.data)
