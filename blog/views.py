from django.shortcuts import redirect
from .models import Post, Topic
from django.views import View, generic as views
from .forms import CreatePostForm, UpdatePostForm
from django.urls import reverse_lazy


class PostMixinView(View):
    model = Post
    success_url = reverse_lazy('blog-home')


class PostsListView(views.ListView):
    model = Topic
    template_name = 'blog/blog_home.html'

    context_object_name = 'topics'


class AllPostsFromTopicView(views.ListView):
    model = Post
    template_name = 'blog/all_posts.html'
    context_object_name = 'posts'
    paginate_by = 6

    def get_queryset(self, **kwargs):
        queryset = Post.objects.filter(topic__title=self.kwargs['topic'])
        return queryset


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
            return redirect('blog-home')


class PostUpdateView(PostMixinView, views.UpdateView):
    template_name = 'blog/post_update.html'
    form_class = UpdatePostForm


class PostDeleteView(PostMixinView, views.DeleteView):
    template_name = 'blog/post_delete.html'
    fields = '__all__'
