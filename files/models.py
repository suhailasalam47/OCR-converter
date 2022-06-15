from django.db import models

# Create your models here.
class Folder(models.Model):
    folder_name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.folder_name


class FolderImage(models.Model):
    folder_img = models.ImageField(upload_to='folder_images/', blank=True)
    slug = models.SlugField(max_length=50, unique=True)
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE)


class FolderText(models.Model):
    folder_text = models.TextField(max_length=5000)   
    slug = models.SlugField(max_length=50, unique=True) 
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE)
    