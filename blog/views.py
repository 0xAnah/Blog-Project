from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.core.paginator import Paginator
from django.views.generic import ListView
from .models import Post

# Create your views here.

class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'


def post_list(request):
    """ 
    This is a function based view for the post list but it is 
    not in use by any url or template the above class based view is
    used in place of it but I left it because as at this time I prefer
    function based view over class based views, I think they are simpler
    to write and undersatnd as compared to class based view that has abstracted
    a lot of functionality. But it is important to note that class based views
    saves us from a lot of redundant code.
    """
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
