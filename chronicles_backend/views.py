import json
import requests
from django.contrib.auth import login
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from .permissions import *
from .serializers import *


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ChronicleUser.objects.all()
    serializer_class = UserSerializer

    @action(methods=['POST', 'OPTIONS'], detail=False, url_name='token', url_path='token')
    def token_parser(self, request):
        data = json.loads(request.body.decode('utf-8'))
        try:
            auth_code = data['code']
        except:
            return HttpResponse('Failed')
        payload = {
            'client_id': 'nUeXTqAt8eJEwfmgZ9vIRSTyexUldebZO8Ht43H0',
            'client_secret': 'xxx',
            'grant_type': 'authorization_code',
            'redirect_url': 'http://localhost:3000',
            'code': auth_code,
        }
        response = requests.post('https://internet.channeli.in/open_auth/token/', data=payload)
        resdict = json.loads(response.text)
        access_token = resdict['access_token']

        response2 = requests.get("https://internet.channeli.in/open_auth/get_user_data/",
                                 headers={'Authorization': f'Bearer {access_token}'})
        resdict2 = json.loads(response2.text)

        # Login
        roles = resdict2['person']['roles']
        maintainer = False
        for i in roles:
            if i['role'] == 'Maintainer':
                maintainer = True
        if maintainer:
            try:
                user = ChronicleUser.objects.get(enrNo=resdict2['student']['enrolmentNumber'])
                login(request=request, user=user)
            except ChronicleUser.DoesNotExist:
                user = ChronicleUser(
                    username=resdict2['person']['fullName'],
                    enrNo=resdict2['student']['enrolmentNumber'],
                    email=resdict2['contactInformation']['instituteWebmailAddress']
                )
                user.save()
                login(request=request, user=user)
        return HttpResponse("Accepted")


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

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        if ChronicleUser.objects.get(pk=request.data['person_in_charge']) in self.get_object().project.team.all():
            return self.update(request, *args, **kwargs)
        else:
            content = {
                'status': 'Not a team member'
            }
            return Response(content)

    def update(self, request, *args, **kwargs):
        if ChronicleUser.objects.get(pk=request.data['person_in_charge']) in self.get_object().project.team.all():
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)
        else:
            content = {
                'status': 'Not a team member'
            }
            return Response(content)


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
