from django.urls import path
from . import views

urlpatterns = [
    path('', views.featured_posts, name='blog-home'),
    path('posts/', views.all_posts, name='all-posts'),
    path('post/<str:pk>', views.post_detail, name='post-detail'),
]