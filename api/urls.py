from django.urls import path
from . import views

urlpatterns = [
    path('', views.getRoutes),
    path('projects/', views.get_projects),
    path('projects/<str:pk>', views.get_project),
]