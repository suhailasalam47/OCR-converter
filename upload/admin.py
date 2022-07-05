from django.contrib import admin
from .models import ImageUploader, PdfUploader

class ImageUploaderAdmin(admin.ModelAdmin):
    list_display = ['user','image_to_convert', 'created_at', 'updated_at']

# Register your models here.
admin.site.register(ImageUploader, ImageUploaderAdmin)
admin.site.register(PdfUploader)
