from django.db import models
from django.contrib.auth.models import User
from PIL import Image
import io

class Photo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='photos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.uploaded_at}"

    def save(self, *args, **kwargs):
        # Суретті сақтамас бұрын EXIF-ті түзету
        if self.image:
            try:
                img = Image.open(self.image)
                exif = img._getexif()
                if exif:
                    orientation = exif.get(274)
                    if orientation:
                        if orientation == 3:
                            img = img.rotate(180, expand=True)
                        elif orientation == 6:
                            img = img.rotate(270, expand=True)
                        elif orientation == 8:
                            img = img.rotate(90, expand=True)
                        img_io = io.BytesIO()
                        img.save(img_io, format='JPEG', quality=95)
                        self.image.save(self.image.name, content=img_io, save=False)
            except Exception:
                pass
        super().save(*args, **kwargs)