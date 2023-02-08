from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_posted = models.DateField(auto_now_add=True)
    content = models.TextField(max_length=280)
    image = models.FileField(upload_to='post_images/', blank=True, null=True)
    likes = models.ManyToManyField(User, related_name='posts')

    def total_likes(self):
        return self.likes.count()
    
    def liking_users_list(self):
        return [{'username': user.username,
                 'display_name': user.profile.display_name,
                 'pfp_url': user.profile.profile_picture.url
                 } for user in self.likes.all()]
    
    def __str__(self) -> str:
        return f'Post by {self.author} on {self.date_posted} - {self.content[0:21]}'
    
    def get_absolute_url(self):
        return reverse("post-detail", kwargs={"pk": self.pk}) 
    