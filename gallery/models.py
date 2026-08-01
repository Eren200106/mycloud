from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

class Photo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='photos')
    image = CloudinaryField('image')  # Cloudinary-да сақталады
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.uploaded_at}"