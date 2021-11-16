from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    created = models.DateTimeField(auto_now_add=True)
    post = models.CharField(max_length=280)
    likes = models.PositiveIntegerField(default=0)

    def serialize(self):
        return {
                "id": self.id,
                "user": self.user.username,
                "created": self.created.strftime("%b %d %Y, %I:%M %p"),
                "post": self.post,
                "likes": self.likes
            }