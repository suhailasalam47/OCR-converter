from .models import Folder


def folder_menu(request):
    links = Folder.objects.all()
    return dict(links=links)