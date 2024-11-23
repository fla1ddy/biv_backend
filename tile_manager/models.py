from django.db import models

class UploadedImage(models.Model):
    image = models.ImageField(upload_to='images/')
    upload_time = models.DateTimeField(auto_now_add=True)
    source = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.image.name
