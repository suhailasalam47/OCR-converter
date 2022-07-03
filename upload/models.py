from django.db import models

from account.models import Account


class ImageUploader(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    image_to_convert = models.ImageField(upload_to='images/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    



    