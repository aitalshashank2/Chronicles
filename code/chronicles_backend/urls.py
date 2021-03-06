from django.urls import path, include
from rest_framework.routers import DefaultRouter
from chronicles_backend.views import *
from django.conf.urls import include

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'projects', ProjectViewSet)
router.register(r'bugReports', BugReportViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'images', ImageViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('projects/<int:pk>/team/', MembersOfProject.as_view()),
    path('projects/<int:pk>/bugReports/', BugsOfProject.as_view()),
    path('bugReports/<int:pk>/comments/', CommentsOnBugs.as_view()),
]

