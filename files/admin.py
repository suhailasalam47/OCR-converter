from django.contrib import admin
from .models import Folder, Content
# Register your models here.


class FolderAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('folder_name',)}

class ContentAdmin(admin.ModelAdmin):
    list_display = [ 'file_name','folder','folder_img']
    prepopulated_fields= {'slug':('file_name',)}   

admin.site.register(Folder, FolderAdmin)
admin.site.register(Content, ContentAdmin)
