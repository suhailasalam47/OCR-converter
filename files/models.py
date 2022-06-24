from django.urls import reverse
from django.db import models

from account.models import Account

# Create your models here.
class Folder(models.Model):
    folder_name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)

    def get_url(self):
        return reverse("folder_category", args=[self.slug])

    def __str__(self):
        return self.folder_name


class Content(models.Model):
    folder_text = models.TextField(max_length=5000)
    slug = models.SlugField(max_length=50)
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE)
    file_name = models.CharField(max_length=50, unique=True)
    folder_img = models.ImageField(upload_to="folder_images/", blank=True)

    def get_url(self):
        return reverse("file_path", args=[self.folder.slug, self.slug])

    def __str__(self):
        return self.file_name
