from django.urls import path
from . import views

from rest_framework_simplejwt.views import(
    TokenObtainPairView, # generate a JWT token based on the user
    TokenRefreshView, # generate a refresh token
)

urlpatterns = [
    path('users/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('', views.getRoutes),
    path('projects/', views.get_projects),
    path('projects/<str:pk>/', views.get_project),
    path('projects/<str:pk>/vote/', views.project_vote),

    path('remove-tag/', views.remove_tag),
    path('remove-message/', views.remove_message),
]