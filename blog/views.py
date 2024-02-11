import logging
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.urls import reverse
from blog.models import Post
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie, vary_on_headers
from blog.forms import CommentForm

logger = logging.getLogger(__name__)

# Create your views here.

def get_ip(request):
  from django.http import HttpResponse
  return HttpResponse(request.META["REMOTE_ADDR"])

def index(request):
    posts = (Post.objects.filter(published_at__lte=timezone.now())
              .order_by("-published_at")
              .select_related("author"))
    logger.debug(f"Got %d posts", len(posts))
    return render(request, "blog/index.html", {"posts": posts})

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.user.is_active:
        if request.method == "POST":
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.content_object = post
                comment.creator = request.user
                comment.save()
                logger.info("Created a comment on post %d from user %s", post.pk, request.user)
                return redirect(request.path_info)
            logger.warn("User %s couldn't create a post because of validation", request.user)
        else:
            comment_form = CommentForm()
    else:
        comment_form = None
    return render(request, "blog/post-detail.html", {"post": post,
                                                   "comment_form": comment_form})

def post_table(request):
  return render(request, "blog/post-table.html", {"post_list_url": reverse("post-list")})
