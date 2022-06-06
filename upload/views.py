from django.shortcuts import render
from .forms import *

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
	else:
		form = ConverterForm()
	context={
		'text':text_from_image,
		'form':form,
		'instance': instance,
	}
	return render(request, 'upload.html', context)

