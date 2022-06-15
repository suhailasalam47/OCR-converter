from django.contrib import admin
from .models import Folder, FolderImage, FolderText
# Register your models here.


class FolderAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('folder_name',)}

admin.site.register(Folder, FolderAdmin)
admin.site.register(FolderImage)
admin.site.register(FolderText)
