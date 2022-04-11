from django.urls import path

from . import views

urlpatterns = [
    # MASS VIEWS
    path('', views.PostsListView.as_view(), name='blog-home'),
    # path('posts/', views.AllPostsView.as_view(), name='all-posts'),
    path('posts/<str:topic>', views.AllPostsFromTopicView.as_view(), name='topic-posts'),
    path('post/<str:pk>', views.SinglePostView.as_view(), name='post-detail'),
    # CRUD OPERATIONS
    path('post/create/', views.PostCreateView.as_view(), name='post-create'),
    path('post/update/<str:pk>', views.PostUpdateView.as_view(), name='post-update'),
    path('post/delete/<str:pk>', views.PostDeleteView.as_view(), name='post-delete'),
]
