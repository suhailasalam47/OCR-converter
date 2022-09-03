from .models import PdfUploader
from django import forms

class PdfForm(forms.ModelForm):
    class Meta:
        model = PdfUploader
        fields = ['pdf_file',]