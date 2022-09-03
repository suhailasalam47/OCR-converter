from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("convert/", views.convert, name="convert"),
    path("uploader", views.uploader, name="uploader"),
    path("pdf_upload", views.pdf_upload, name="pdf_upload"),
    path("folders_list/", views.folders_list, name="folders_list"),
    path(
        "folders_list/<slug:folder_slug>/",
        views.documents_save,
        name="folder_category",
    ),
    path(
        "folders_list/<slug:folder_slug>/<slug:file_slug>/",
        views.file_path,
        name="file_path",
    ),
]
