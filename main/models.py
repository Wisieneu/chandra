from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_posted = models.DateField(auto_now_add=True)
    content = models.TextField(max_length=280)
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    likes = models.ManyToManyField(User, related_name='posts', blank=True)
    
    @property
    def likes_amount(self):
        return self.likes.count()

    @property
    def liking_users_list(self):
        return {user.id: {'username': user.username,
                 'display_name': user.profile.display_name,
                 'profile_picture': user.profile.profile_picture.url
                 } for user in self.likes.all()}

    @property
    def comments_amount(self):
        return self.comments.count()

    def __str__(self) -> str:
        return f'Post by {self.author.profile} on {self.date_posted}: {self.content}'

    def get_absolute_url(self):
        return reverse("post-detail", kwargs={"post_id": self.pk})


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default='Chandra User')
    date_added = models.DateField(auto_now_add=True)
    content = models.TextField(max_length=280)
    image = models.ImageField(upload_to='comment_images/', blank=True, null=True)
    likes = models.ManyToManyField(User, related_name='comments_likes')

    @property
    def likes_amount(self):
        return self.likes.count()

    @property
    def liking_users_list(self):
        return {user.id: {'username': user.username,
                 'display_name': user.profile.display_name,
                 'profile_picture': user.profile.profile_picture.url
                 } for user in self.likes.all()}
    
    @property
    def image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url

    def get_absolute_url(self):
        return reverse("post-detail", kwargs={"post_id": self.post.id})

    def __str__(self):
        return f'{self.post} => comment by {self.author.profile} on {self.date_added}: {self.content}'