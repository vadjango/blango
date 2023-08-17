from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.utils.translation import gettext_lazy as _

class BlangoUserManager(UserManager):
  def _create_user(self, email=None, password=None, **kwargs):
    if email is None:
      raise ValueError("User must have an email!")
    if password is None:
      raise ValueError("User must have a password!")
    email = self.normalize_email(email)
    user = self.model(email=email, **kwargs)
    user.set_password(password)
    user.save(using=self._db)
    return user

  def create_user(self, email, password, **kwargs):
    kwargs.setdefault("is_staff", False)
    kwargs.setdefault("is_superuser", False)
    return self._create_user(email, password, **kwargs)

  def create_superuser(self, email, password, **kwargs):
    kwargs.setdefault("is_staff", True)
    kwargs.setdefault("is_superuser", True)

    if kwargs.get("is_staff") is not True:
      raise ValueError("Superuser must have is_staff=True")
    if kwargs.get("is_superuser") is not True:
      raise ValueError("Superuser must have is_superuser=True")

    return self._create_user(email, password, **kwargs)

class User(AbstractUser):
  username = None
  email = models.EmailField(_("email address"), unique=True)
  
  objects = BlangoUserManager()

  USERNAME_FIELD = "email"
  REQUIRED_FIELDS = []

  def __str__(self):
    return self.email
