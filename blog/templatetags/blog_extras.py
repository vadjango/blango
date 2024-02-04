from blog.models import Post
from django import template
from django.contrib.auth import get_user_model
import logging
from django.utils.html import format_html
from django.core.cache import cache

User = get_user_model()

register = template.Library()
logger = logging.getLogger(__name__)


@register.filter
def author_details(author, current_user):
  if not isinstance(author, User):
    return ""
  if author == current_user:
    return format_html("<strong>me</strong>")
  elif author.first_name and author.last_name:
    name = f"{author.first_name} {author.last_name}"
  elif author.username:
    name = author.username
  else:
    name = author.email
  prefix = format_html('<a href="mailto:{}">', author.email)
  suffix = format_html('</a>')
  return format_html("{}{}{}", prefix, name, suffix)

@register.simple_tag
def row(extra_classes=""):
  return format_html('<div class="row {}">', extra_classes)

@register.simple_tag
def endrow():
  return format_html('</div>')

@register.simple_tag
def col(extra_classes=""):
  return format_html('<div class="col {}">', extra_classes)

@register.simple_tag
def endcol():
  return format_html('</div>')


def get_recent_posts(post):
  posts = Post.objects.exclude(pk=post.pk).order_by("-published_at")[:5]
  logger.debug(f"Loaded {len(posts)} recent post for post {post}")
  return posts


@register.inclusion_tag("blog/post-list.html")
def recent_posts(post):
  posts = cache.get_or_set(f"recent_posts_exclude_post_{post.pk}", get_recent_posts(post))
  logger.debug(posts)
  return {"title": "Recent Posts", "posts": posts}
