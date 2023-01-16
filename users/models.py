from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    display_name = models.CharField(max_length=32)
    profile_picture = models.ImageField(default='default.jpg', upload_to='profile_pictures')
    

    def __str__(self) -> str:
        if self.first_name and self.last_name:
            return f'{self.first_name} {self.last_name} - {self.user.username} ({self.display_name}) profile'
        else:
            return f'{self.user.username} ({self.display_name}) Profile'