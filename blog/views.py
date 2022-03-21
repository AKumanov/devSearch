import re
from users.models import Profile
from django.shortcuts import render, redirect
from .models import Post
from django.views import View, generic as views
from .forms import CreatePostForm
from django.urls import reverse_lazy
from .utils import paginate_posts, search_posts

class PostMixinView(View):
    model = Post
    success_url = reverse_lazy('all-posts')

class PostsListView(views.ListView):
    model = Post
    template_name = 'blog/blog_home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        featured_posts = Post.objects.filter(is_featured=True)[0:5]
        context['featured_posts'] = featured_posts
        return context


class AllPostsView(views.ListView):
    model = Post
    template_name = 'blog/all_posts.html'
    context_object_name = 'posts'
    paginate_by = 6
    # paginate_by = 6

    def get_queryset(self):
        return super().get_queryset()
        
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        request = self.request
        posts, search_query = search_posts(request)
        custom_range, posts = paginate_posts(request, posts, 9)
        context['custom_range'] = custom_range
        context['posts'] = posts
        context[' search_query'] = search_query
        return context
    

class SinglePostView(views.DetailView):
    model = Post
    template_name = 'blog/post_detail.html'


class PostCreateView(PostMixinView, views.CreateView):
    template_name = 'blog/create_post.html'
    form_class = CreatePostForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.owner = request.user.profile
            post.save()
            return redirect('all-posts')
    

class PostUpdateView(PostMixinView, views.UpdateView):
    template_name = 'blog/post_update.html'
    fields = '__all__'


class PostDeleteView(PostMixinView, views.DeleteView):
    template_name = 'blog/post_delete.html'
    fields = '__all__'