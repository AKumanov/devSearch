from django.contrib import admin

from projects.models import Project
from .models import Project, Review, Tag


admin.site.register(Project)
admin.site.register(Review)
admin.site.register(Tag)

