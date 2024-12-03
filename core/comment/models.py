from django.db import models
from core.abstract.models import AbstractModel, AbstractManager

# Create your models here.


class CommentManager(AbstractManager):
    pass


class Comment(AbstractModel):
    post = models.ForeignKey(
        "core_post.Post", on_delete=models.PROTECT, related_name="post_comments"
    )
    author = models.ForeignKey(
        "core_user.User", on_delete=models.PROTECT, related_name="author_comments"
    )
    body = models.TextField()
    edited = models.BooleanField(default=False)

    objects = CommentManager()

    class Meta:
        db_table = "comments"
        verbose_name = "Comment"
        verbose_name_plural = "Comments"

    def __str__(self):
        return f"{self.author.username} - {self.post.body[:10]} - {self.body[:20]}"
