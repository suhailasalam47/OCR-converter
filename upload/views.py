from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from files.models import Folder, Content
from .models import ImageUploader
from PIL import Image
from wand.image import Image as wi
import pytesseract
from pdf2image import convert_from_path
from project import settings
from .forms import PdfForm


def index(request):
    return render(request, "index.html")
    

def convert(request):
    if request.method == 'POST':
        if 'image_btn' in request.POST:
            return redirect("uploader")
        else:
            return redirect("pdf_upload")
    return render(request, "convert/convert.html")


def pdf_upload(request):
    text_from_pdf=None
    image=None
    if request.method == "POST":
        form = PdfForm(request.POST, request.FILES)
        if form.is_valid():
            pdf_file = request.FILES['pdf_file']
            obj=form.save()
            new_pdf = obj.pdf_file
            image = pdf_to_img(new_pdf)
            text_from_pdf=success(image)
            
            if text_from_pdf:
                request.session["text"] = text_from_pdf
            else:
                messages.error(request, "no text!!")
                return redirect("pdf_upload")
    else:
        form = PdfForm()
    context = {
        'form':form,
        'text':text_from_pdf,
        'image':image,
    }
    return render(request, 'convert/pdf_upload.html',context)


def pdf_to_img(new_pdf):
    path= settings.MEDIA_ROOT  + '/' + str(new_pdf)
    images = convert_from_path(path,fmt='png',dpi=300,grayscale=True)
    image = images[0]
    image.save("imagen.png")
    img="imagen.png"
    return img


def success(image):
    text = pytesseract.image_to_string(Image.open(image))
    return text


# Create your views here.
def uploader(request):
    text_from_image = None
    if request.method == "POST":
        img = request.FILES["uploaded_img"]
        images = ImageUploader()
        images.image_to_convert = img
        images.save()
        text_from_image = success(img)

        if text_from_image and img:
            request.session["text"] = text_from_image
        else:
            messages.error(request, "no text!!")
            return redirect("uploader")

    context = {
        "text": text_from_image,
    }
    return render(request, "convert/upload.html", context)


@login_required(login_url="login")
def save_document(request):
    if request.method == "POST":
        is_img_save = request.POST.get("checkbox")
        request.session["is_save"] = is_img_save
        user = request.user
        folder = Folder.objects.filter(user=user)
    else:
        user = request.user
        folder = Folder.objects.filter(user=user)
    context = {
        "folder": folder,
    }
    return render(request, "files/file_list.html", context)


@login_required(login_url="login")
def folder_uploads(request, folder_slug=None):
    categories = None
    item = None
    text_from_image = None
    print(folder_slug)
    if folder_slug != None:
        categories = get_object_or_404(Folder, slug=folder_slug)
        print(categories)
        item_list = Content.objects.filter(folder=categories)
        print(item_list)

        if request.method == "POST":
            file_name = request.POST["file_name"]
            item = Content()
            text_from_image = request.session["text"]
            item.folder_text = text_from_image
            item.folder = categories
            item.file_name = file_name
            item.slug = file_name
            item.save()
            messages.success(request, "Document saved successfully")
            # return redirect('save_document')
        # else:
        # 	item_list = Content.objects.filter(folder=categories)
    else:
        return redirect("save_document")

    context = {
        "item": item,
        "text": text_from_image,
        "objects": item_list,
    }
    print("folder", item_list)
    return render(request, "files/file_contents.html", context)


def file_path(request, folder_slug, file_slug):
    single_file = Content.objects.get(
        folder__slug=folder_slug, slug=file_slug
    )
    check = request.session["is_save"]
    context = {
        "single_file": single_file,
        "check": check,
    }
    print("single file", single_file)
    return render(request, "files/file_path.html", context)
