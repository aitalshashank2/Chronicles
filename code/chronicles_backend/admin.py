from django.contrib import admin
from .models import *


admin.site.register(ChronicleUser)
admin.site.register(Project)
admin.site.register(BugReport)
admin.site.register(Comment)
admin.site.register(Image)
