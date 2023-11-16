from rest_framework import serializers
from blog.models import Post, Tag
from blango_auth.models import User
from rest_framework.reverse import reverse


class AuthorPostHyperlinkField(serializers.HyperlinkedRelatedField):
  view_name = "api_post_detail"
  queryset = Post.objects.all()

  def get_url(self, obj, view_name, request, format):
    url_kwargs = {
      "author_email": obj.author.email,
      "post_id": obj.pk
    }
    return reverse(view_name, kwargs=url_kwargs, request=request, format=format)

  def get_object(self, view_name, view_args, view_kwargs):
    lookup_kwargs = {
      "author__email": view_kwargs["author_email"],
      "pk": view_kwargs["post_id"]
    }
    return self.get_queryset().get(**lookup_kwargs)



class PostSerializer(serializers.ModelSerializer):
  tags = serializers.SlugRelatedField(queryset=Tag.objects.all(), 
                                      many=True,
                                      slug_field="value")
  author = serializers.HyperlinkedRelatedField(queryset=User.objects.all(),
                                               view_name="api_user_detail",
                                               lookup_field="email")


  class Meta:
    model = Post
    fields = "__all__"
    readonly = ["modified_at", "created_at"]


class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ["first_name", "last_name", "email"]
