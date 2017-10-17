from django.db import models


# Create your models here.
class Post(models.Model):
    photo = models.ImageField(upload_to='photo', max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)


class PostComment(models.Model):
    post = models.ForeignKey(
        Post,
        # blank=True,
        # null=True,
        related_name='comments',
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # 가장 나중에 달린 Comment가 가장 나중에 오도록 ordering설정
        ordering = [ 'created_at']