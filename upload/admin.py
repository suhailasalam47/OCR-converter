from django.contrib import admin
from .models import ImageUploader

class ImageUploaderAdmin(admin.ModelAdmin):
    list_display = ['image_to_convert', 'created_at', 'updated_at', 'is_save']

# Register your models here.
admin.site.register(ImageUploader, ImageUploaderAdmin)
