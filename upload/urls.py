from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("convert/", views.convert, name="convert"),
    path("uploader", views.uploader, name="uploader"),
    path("pdf_upload", views.pdf_upload, name="pdf_upload"),
    path("save_document/", views.save_document, name="save_document"),
    path(
        "save_document/<slug:folder_slug>/",
        views.folder_uploads,
        name="folder_category",
    ),
    path(
        "save_document/<slug:folder_slug>/<slug:file_slug>/",
        views.file_path,
        name="file_path",
    ),
]
