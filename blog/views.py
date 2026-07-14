from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.core.paginator import Paginator
from django.views.generic import ListView
from django.views.decorators.http import require_POST
from django.core.mail import send_mail
from .models import Post
from .forms import EmailPostForm, CommentForm

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
    # List of active comments for this post
    comments = post.comments.filter(active=True)
    # Form for users to comment
    form = CommentForm()
    
    context = {'post':post, 'comments': comments, 'form': form}
    return render(request, 'blog/post/detail.html', context=context)

def post_share(request, post_id):

    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISH)
    sent = False

    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # form field pass validation
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} {cd['email']} recommends you read {post.title}"
            message = f"Read {post.title} at {post_url}\n\n {cd['name']}\'s comments: {cd['comment']}"
            send_mail(subject=subject, message=message, from_email=None, recipient_list=[cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    
    context = {'post':post, 'form':form, 'sent':sent}
    return render(request, 'blog/post/share.html', context=context)

@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISH)
    comment = None
    # a comment was posted
    form = CommentForm(request.POST)
    if form.is_valid():
        # create a comment object without saving to the database
        comment = form.save(commit=False)
        # assign the post to the comment
        comment.post = post
        # save the comment to the database
        comment.save()
    
    context = {'post':post, 'form': form, 'comment':comment}
    return render(request, 'blog/post/comment.html', context=context)