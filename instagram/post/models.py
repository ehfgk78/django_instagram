from django.db import models

# Create your models here.
class Post(models.Model):
    photo = models.ImageField(upload_to='photo', max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

class PostComment(models.Model):
    post = models.ForeignKey(
        Post,
        blank=True,
        null=True,
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)