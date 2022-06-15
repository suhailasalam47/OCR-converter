from django.shortcuts import get_object_or_404, render
from .forms import *
from django.contrib.auth.decorators import login_required
from files.models import Folder, FolderImage, FolderText


try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract


def index(request):
    return render(request, 'index.html')


def success(image):
	text = pytesseract.image_to_string(Image.open(image))  
	return text

# Create your views here.
def uploader(request):
	text_from_image=None
	instance = None
	if request.method == 'POST':
		form = ConverterForm(request.POST, request.FILES)

		if form.is_valid():
			img = form.cleaned_data.get('image_to_convert')
			text_from_image=success(img)
			
			instance = form.save()
			print(text_from_image)
			
			request.Session['text'] = text_from_image
	else:
		form = ConverterForm()
	context={
		'text':text_from_image,
		'form':form,
		'instance': instance,
	}
	
	return render(request, 'upload.html', context)


@login_required(login_url='login')
def save_document(request):
    folder = Folder.objects.all()
    context ={
        'folder':folder,
    }
	
    return render(request, 'files/file_list.html', context)


def folder_uploads(request):
	text_from_image= request.Session['text']
	context = {
		'text' : text_from_image,
	}
	return render(request, 'files/file_contents.html',context)
