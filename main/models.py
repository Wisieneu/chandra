from django.db import models
from users.models import User


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_posted = models.DateField()
    content = models.TextField()

    def __str__(self) -> str:
        return f'Post by {self.author} on {self.date_posted} - {self.content[0:21]}'