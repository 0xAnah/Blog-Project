from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.core.paginator import Paginator
from .models import Post

# Create your views here.

def post_list(request):
    posts = Post.published.all()

    paginator = Paginator(posts, 3)
    page_number = request.GET.get('page', 1)
    posts = paginator.get_page(page_number)
    context = {'posts':posts}

    return render(request, 'blog/post/list.html', context=context)


def post_detail(request, year, month, day, post):
    post = get_object_or_404(
        Post, status=Post.Status.PUBLISH, publish__year=year, publish__month=month, publish__day=day, slug=post
    )
    
    context = {'post':post}
    return render(request, 'blog/post/detail.html', context=context)
