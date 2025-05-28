from django.db import models
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.postgres.fields import ArrayField
# Create your models here.

class Blogpost(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blogposts')
    title = models.CharField(max_length=100)
    content = models.TextField(max_length=1000000, blank=True)
    image = CloudinaryField('image', blank=True, null=True)
    category = models.CharField(max_length=100, blank=True, null=True)
    tags = ArrayField(
        models.CharField(max_length=50, blank=True),
        default=list,
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)

    @property
    def like_count(self):
        return self.likes.count()
   

class Comment(models.Model):
    post = models.ForeignKey('Blogpost', related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title}"


class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('like', 'Like'),
        ('comment', 'Comment'),
    )
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='notifications', on_delete=models.CASCADE)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sent_notifications', on_delete=models.CASCADE)
    post = models.ForeignKey('Blogpost', on_delete=models.CASCADE)
    notification_type = models.CharField(max_length=10, choices=NOTIFICATION_TYPES)
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
