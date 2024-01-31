from datetime import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from pytz import UTC
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from blog.models import Post


class PostApiTestCase(TestCase):
  def setUp(self):
    self.u1 = get_user_model().objects.create_user(email="test@example.com",
                                              password="password1")
    self.u2 = get_user_model().objects.create_user(email="test2@example.com",
                                              password="password2")

    posts = [
      Post.objects.create(author=self.u1, 
                          published_at=timezone.now(), 
                          title="Post-title-1", 
                          slug="post-slug-1", 
                          summary="It's a first summary",
                          content="Here we go!"),
      Post.objects.create(author=self.u2,
                          published_at=timezone.now(), 
                          title="Post-title-2", 
                          slug="post-slug-2", 
                          summary="It's a second summary",
                          content="Here we go again!")
    ]                                     

    self.post_lookup = {p.id: p for p in posts}
    self.client = APIClient()
    token = Token.objects.create(user=self.u1)
    self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
  
  def test_post_list(self):
    response = self.client.get("/api/v1/posts/")
    data = response.json()["results"]
    self.assertEqual(len(data), 2)

    for post_dict in data:
      post_obj = self.post_lookup[post_dict["id"]]
      self.assertEqual(post_obj.title, post_dict["title"])
      self.assertEqual(post_obj.slug, post_dict["slug"])
      self.assertEqual(post_obj.summary, post_dict["summary"])
      self.assertEqual(post_obj.content, post_dict["content"])
      self.assertTrue(post_dict["author"].endswith(f"/api/v1/users/{post_obj.author.email}"))
      self.assertEqual(
        post_obj.published_at,
        datetime.strptime(post_dict["published_at"], "%Y-%m-%dT%H:%M:%S.%fZ")
        .replace(tzinfo=UTC)
      )

  def test_unauthenticated_post_create(self):
    self.client.credentials()
    post_dict = {
      "title": "Test Post",
      "slug": "test-post",
      "summary": "This is a summary",
      "content": "Hello, guys",
      "published_at": "2021-01-10T09:00:00Z",
      "author": "http://testserver/api/v1/users/test@example.com"
    }
    response = self.client.post("/api/v1/posts/", post_dict)
    self.assertEqual(response.status_code, 401)
    self.assertEqual(Post.objects.all().count(), 2)

  def test_post_create(self):
    post_dict = {
      "title": "Test Post",
      "slug": "test-post",
      "summary": "This is a summary",
      "content": "Hello, guys",
      "published_at": "2021-01-10T09:00:00Z",
      "author": "http://testserver/api/v1/users/test@example.com"
    }
    response = self.client.post("/api/v1/posts/", post_dict)
    post_id = response.json()["id"]
    post = Post.objects.get(pk=post_id)
    self.assertEqual(post.title, post_dict["title"])
    self.assertEqual(post.slug, post_dict["slug"])
    self.assertEqual(post.summary, post_dict["summary"])
    self.assertEqual(post.content, post_dict["content"])
    self.assertEqual(post.title, post_dict["title"])
    self.assertEqual(post.author, self.u1)
    self.assertEqual(post.published_at, datetime(2021, 1, 10, 9, 0, 0, tzinfo=UTC))