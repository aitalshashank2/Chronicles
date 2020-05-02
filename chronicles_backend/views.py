from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from .permissions import *
from .serializers import *


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ChronicleUser.objects.all()
    serializer_class = UserSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated, IsProjectCreatorOrAdmin]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class BugReportViewSet(viewsets.ModelViewSet):
    queryset = BugReport.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsTeamMemberOrAdmin]

    def perform_create(self, serializer):
        serializer.save(reporter=self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return BugReportSerializer
        else:
            return BugReportEditSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsCommenter]

    def perform_create(self, serializer):
        serializer.save(commenter=self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CommentSerializer
        else:
            return CommentEditSerializer


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
