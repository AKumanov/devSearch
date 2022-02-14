from django.contrib import admin

from projects.models import Project
from .models import Project


admin.site.register(Project)
