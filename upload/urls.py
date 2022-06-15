from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('upload', views.uploader, name='upload'),
    path('save_document/', views.save_document, name="save_document"),
    path('folder_uploads/', views.folder_uploads, name='folder_uploads'),
]