from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from core.abstract.models import AbstractModel, AbstractManager

# Create your models here.


class UserManager(BaseUserManager, AbstractManager):

    def create_user(self, email, password, username, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        if not password:
            raise ValueError("The Password field must be set")
        if not username:
            raise ValueError("The Username field must be set")
        user = self.model(
            email=self.normalize_email(email), username=username, **extra_fields
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, username, **extrafields):
        if not email:
            raise ValueError("The Email field must be set")
        if not password:
            raise ValueError("The Password field must be set")
        if not username:
            raise ValueError("The Username field must be set")
        user = self.create_user(email, password, username, **extrafields)
        user.is_admin = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin, AbstractModel):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    posts_liked = models.ManyToManyField(
        to="core_post.Post",
        related_name="liked_by",
        null=True,
        blank=True,
    )

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.email

    def like(self, post):
        return self.posts_liked.add(post)

    def remove_like(self, post):
        return self.posts_liked.remove(post)

    def has_liked(self, post):
        return self.posts_liked.filter(pk=post.pk).exists()
