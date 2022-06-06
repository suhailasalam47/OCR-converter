from django.db import models


class ImageUploader(models.Model):
    name = models.CharField(max_length=100)
    image_to_convert = models.ImageField(upload_to='images/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_save = models.BooleanField(default=False)
    
    

    