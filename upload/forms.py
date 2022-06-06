from django import forms
from .models import *

class ConverterForm(forms.ModelForm):

	class Meta:
		model = ImageUploader
		fields = ['image_to_convert',]
