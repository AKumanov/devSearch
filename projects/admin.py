from django.contrib import admin

from projects.models import Project
from .models import Project, Review, Tag


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title',)
    list_filter = ('owner',)
    search_fields = ('title',)
    search_help_text = 'Search by Project Title'

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    pass


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass


