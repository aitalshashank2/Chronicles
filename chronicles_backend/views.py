import json
import requests
from decouple import config
from django.contrib.auth import login, logout
from django.http import JsonResponse, HttpResponseForbidden, HttpResponseBadRequest
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from .permissions import *
from .serializers import *
from .mailingWizard import MailThread


class UserViewSet(viewsets.ModelViewSet):
    queryset = ChronicleUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]

    @action(methods=['GET'], detail=False, url_path='projects', url_name='projects')
    def user_projects(self, request):
        if request.user.is_authenticated and request.user.is_active:
            serializer = ProjectSerializer(request.user.projects.all(), many=True)
            return Response(serializer.data)
        else:
            return HttpResponseForbidden()

    @action(methods=['GET'], detail=False, url_path='bugReports', url_name='bugReports')
    def user_bug_reports(self, request):
        if request.user.is_authenticated and request.user.is_active:
            serializer = BugReportVerboseSerializer(request.user.bugs_assigned.all(), many=True)
            return Response(serializer.data)
        else:
            return HttpResponseForbidden()

    @action(methods=['GET'], detail=False, url_path='curr', url_name='curr')
    def curr_user(self, request):
        if request.user.is_authenticated:
            user = request.user
            if user.is_active:
                serializer = UserSerializer(user)
                return JsonResponse(serializer.data)
            else:
                return HttpResponseForbidden()

        else:
            return HttpResponseForbidden()

    @action(methods=['GET'], detail=False, url_path='logout', url_name='logout')
    def logoutCU(self, request):
        if request.user.is_authenticated:
            logout(request)
            return JsonResponse({'status': 'Logged out'})
        else:
            return HttpResponseForbidden()

    @action(methods=['POST', 'OPTIONS'], detail=False, url_name='token', url_path='token')
    def token_parser(self, request):
        try:
            data = json.loads(request.body.decode('utf-8'))
            auth_code = data['code']
        except:
            return HttpResponseBadRequest()
        payload = {
            'client_id': config('CLIENT_ID'),
            'client_secret': config('CLIENT_SECRET'),
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
                if user.is_active:
                    login(request=request, user=user)
                else:
                    return HttpResponseForbidden()
            except ChronicleUser.DoesNotExist:
                enr_no = resdict2['student']['enrolmentNumber']
                if (int(enr_no) // (10 ** 6)) % 10 == 6:
                    staff = True
                else:
                    staff = False
                user = ChronicleUser(
                    username=resdict2['person']['fullName'],
                    enrNo=resdict2['student']['enrolmentNumber'],
                    email=resdict2['contactInformation']['instituteWebmailAddress'],
                    is_staff=staff,
                    isAdmin=staff,
                    is_superuser=staff
                )
                user.save()
                login(request=request, user=user)
        return JsonResponse({'user': user.username})


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    lookup_field = 'slug'
    permission_classes = [permissions.IsAuthenticated, IsProjectCreatorOrAdmin]

    def perform_create(self, serializer):
        project = serializer.save(creator=self.request.user)
        context = {
            "action": "new_team_member",
            "project": project,
        }
        MailThread(serializer.validated_data['team'], context).start()

    def perform_update(self, serializer):
        try:
            new_users = [user for user in serializer.validated_data['team'] if user not in self.get_object().team.all()]
            context = {
                "action": "new_team_member",
                "project": self.get_object(),
            }
            MailThread(new_users, context).start()
        except KeyError:
            pass
        serializer.save()


class BugReportViewSet(viewsets.ModelViewSet):
    queryset = BugReport.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsTeamMemberOrAdmin]

    def perform_create(self, serializer):
        bug_report = serializer.save(reporter=self.request.user)
        context = {
            "action": "bug_report_update",
            "project": bug_report.project,
            "bug_report": bug_report,
        }
        MailThread(bug_report.project.team.all(), context).start()

    def perform_update(self, serializer):
        try:
            user = serializer.validated_data['person_in_charge']
            status = serializer.validated_data['status']

            if status:
                context = {
                    "action": "bug_resolved",
                    "project": self.get_object().project,
                    "bug_report": self.get_object(),
                }
                MailThread(self.get_object().project.team.all(), context).start()
            else:
                context = {
                    "action": "bug_report_assignment",
                    "project": self.get_object().project,
                    "bug_report": self.get_object(),
                }
                MailThread([user], context).start()
        except KeyError:
            pass
        serializer.save()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return BugReportSerializer
        elif self.request.method == 'PATCH' or self.request.method == 'PUT':
            return BugReportEditSerializer
        else:
            return BugReportVerboseSerializer

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
        serializer = CommentVerboseSerializer(BugReport.objects.get(pk=pk).comment_set.all(), many=True)
        return Response(serializer.data)


class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(methods=['POST'], detail=False, url_path='deleteRem', url_name='deleteRem')
    def delete_remaining_images(self, request):
        if request.user.is_authenticated:
            # try:
            randIdentifier = request.POST.get('randIdentifier')
            urls = request.POST.get('urls')

            query_set = Image.objects.filter(randIdentifier=randIdentifier)
            for i in query_set:
                if i.url.url not in urls:
                    i.delete()

            return JsonResponse({'status': 'successful'})
            # except:
            #     return HttpResponseBadRequest()
        else:
            return HttpResponseForbidden()
