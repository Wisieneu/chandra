from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    display_name = models.CharField(max_length=32, default=str(user))
    profile_picture = models.ImageField(default='assets/default.jpg', upload_to='profile_pictures')
    

    def __str__(self) -> str:
        if self.first_name and self.last_name:
            return f'{self.first_name} {self.last_name} - {self.user.username} ({self.display_name}) profile'
        else:
            return f'{self.user.username} ({self.display_name}) Profile'
    
    def save(self):
        super().save()
        img = Image.open(self.profile_picture.path)
        if img.height > 360 or img.width > 360:
            output_size = (360, 360)
            img.thumbnail(output_size)
            img.save(self.profile_picture.path)