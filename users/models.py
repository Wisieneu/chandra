from django.db import models
from django.contrib.auth.models import User
from PIL import Image

    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    display_name = models.CharField(max_length=32)
    profile_picture = models.ImageField(default='assets/default.jpg', upload_to='profile_pictures')
    

    def __str__(self) -> str:
        result = f'{self.user.username}'
        if self.display_name:
            result += f' ({self.display_name})'
        return f"{result}'s profile"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.profile_picture.path)
        if img.height > 360 or img.width > 360:
            output_size = (360, 360)
            img.thumbnail(output_size)
            img.save(self.profile_picture.path)