from rest_framework import serializers
from chronicles_backend.models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChronicleUser
        fields = ['id', 'username', 'first_name', 'last_name', 'isAdmin', 'is_active']


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'creator', 'team', 'creation', 'image', 'slug']
        read_only_fields = ['creator', 'creation']
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class BugReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = BugReport
        fields = ['id', 'project', 'reporter', 'heading', 'description',
                  'person_in_charge', 'creation', 'status', 'tagsHash']
        read_only_fields = ['reporter', 'creation', 'status', 'person_in_charge']


class BugReportEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = BugReport
        fields = ['id', 'project', 'reporter', 'heading', 'description',
                  'person_in_charge', 'creation', 'status', 'tagsHash']
        read_only_fields = ['reporter', 'creation', 'project', 'heading', 'description', 'tagsHash']


class BugReportVerboseSerializer(serializers.ModelSerializer):
    reporter = UserSerializer()
    person_in_charge = UserSerializer()

    class Meta:
        model = BugReport
        fields = ['id', 'project', 'reporter', 'heading', 'description',
                  'person_in_charge', 'creation', 'status', 'tagsHash']
        read_only_fields = ['reporter', 'creation', 'project', 'heading', 'description', 'tagsHash']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'report', 'creation', 'commenter', 'body']
        read_only_fields = ['commenter', 'creation']


class CommentEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'report', 'creation', 'commenter', 'body']
        read_only_fields = ['commenter', 'creation', 'report']


class CommentVerboseSerializer(serializers.ModelSerializer):
    commenter = UserSerializer()

    class Meta:
        model = Comment
        fields = ['id', 'report', 'creation', 'commenter', 'body']
        read_only_fields = ['commenter', 'creation']


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'randIdentifier', 'url']

# Tags legend:
# 0 :Functionality
# 1 :Usability
# 2 :Interface
# 3 :Compatibility
# 4 :Performance
# 5 :Security
# 6 :Management
# 7 :Code
# 8 :UI
# 9 :UX
# 10:New Feature
# 11:Fat gaya
# 12:Design
# 13:Front end
# 14:Back end
# 15:Database
# 16:External Resource
# 17:Coverage
# 18:Bug
# 19:Improvement
# 20:Broken
# 21:Cookie
# 22:Typo
# 23:
