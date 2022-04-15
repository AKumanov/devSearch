from django.urls import path, include
from . import views
from users import views as user_views

urlpatterns = [
    path('', views.projects, name='projects'),
    path('project/<str:pk>/', views.project, name='project'),
    path('create/project/', views.create_project, name='create-project'),
    path('update-project/<str:pk>/', views.update_project, name='update-project'),
    path('send-issue/<str:pk>/<str:post_pk>/', user_views.send_issue, name='send-issue'),

    path('delete-project/<str:pk>/', views.delete_project, name='delete-project'),
]