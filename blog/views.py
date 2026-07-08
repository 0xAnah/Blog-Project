from django.shortcuts import render
from django.http import Http404
from .models import Post

# Create your views here.

def post_list(request):
    posts = Post.published.all()
    context = {'posts':posts}

    return render(request, 'blog/post/list.html', context=context)

def post_detail(request, id):

    try:
        post = Post.published.get(id=id)
    except Post.DoesNotExist:
        raise Http404("Post not found")

    context = {'post':post}
    return render(request, 'blog/post/detail.html', context=context)
