from django.shortcuts import render
from .models import Post

# Create your views here.
def featured_posts(request):
    posts = Post.objects.filter(is_featured=True)[0:5]
    print(posts)
    context = {
        'posts': posts        
    }

    return render(request, 'blog/blog_home.html', context)


def all_posts(request):
    posts = Post.objects.all()
    context = {
        'posts': posts,
    }
    return render(request, 'blog/all_posts.html', context)


def post_detail(request, pk):
    post = Post.objects.get(id=pk)
    context = {
        'post': post,
    }
    return render(request, 'blog/post_detail.html', context)