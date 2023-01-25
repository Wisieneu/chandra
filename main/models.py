from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_posted = models.DateField(auto_now_add=True)
    content = models.TextField(max_length=280)
    image = models.FileField(upload_to='post_images/', blank=True, null=True)

    def __str__(self) -> str:
        return f'Post by {self.author} on {self.date_posted} - {self.content[0:21]}'
    
    def get_absolute_url(self):
        return reverse("post-detail", kwargs={"pk": self.pk}) 
    