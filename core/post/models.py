from django.db import models
from core.abstract.models import AbstractManager, AbstractModel

# Create your models here.


class PostManager(AbstractManager):
    pass


class Post(AbstractModel):
    author = models.ForeignKey(to="core_user.User", on_delete=models.CASCADE)
    body = models.TextField()
    edited = models.BooleanField(default=False)

    objects = PostManager()

    def __str__(self):
        return f"{self.author.username} - {self.created} - {self.body[:20]}"
