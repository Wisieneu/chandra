from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from PIL import Image

    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    display_name = models.CharField(max_length=32)
    profile_picture = models.ImageField(default='assets/default.jpg', upload_to='profile_pictures')
    slug = models.SlugField(max_length=150, default=user)

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
    
    def get_absolute_url(self):
        return reverse("profile", kwargs={"pk": self.pk})