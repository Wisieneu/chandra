from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_posted = models.DateField(auto_now_add=True)
    content = models.TextField(max_length=280)
    image = models.FileField(upload_to='post_images/', blank=True, null=True)
    likes = models.ManyToManyField(User, related_name='posts')

    @property
    def total_likes(self):
        return self.likes.count()

    @property
    def liking_users_list(self):
        return [user for user in self.likes.all()]

    @property
    def comments_amount(self):
        return self.comments.count()

    def __str__(self) -> str:
        return f'Post by {self.author.profile} on {self.date_posted}'

    def get_absolute_url(self):
        return reverse("post-detail", kwargs={"pk": self.pk})


class Comment(models.Model):
    post = models.ForeignKey(
        Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(
        User, on_delete=models.SET_DEFAULT, default='Chandra User')
    date_added = models.DateField(auto_now_add=True)
    content = models.TextField(max_length=280)
    # comment_likes = models.ManyToManyField(User)

    def get_absolute_url(self):
        return reverse("post-detail", kwargs={"pk": self.post.id})

    def __str__(self):
        return f'{self.post} => comment by {self.author.profile} on {self.date_added}'