from django.contrib import admin
from .models import *



admin.site.register(Projects)
admin.site.register(Activity)
admin.site.register([Artifact, Member])