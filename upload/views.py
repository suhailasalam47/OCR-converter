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
import pathlib


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

            file= settings.MEDIA_ROOT + '/' + str(new_pdf)
            file_extension = pathlib.Path(file).suffix
            try:
                if file_extension.endswith((".pdf")):
                    image = pdf_to_img(new_pdf)
                    text_from_pdf=success(image)
            except:
                pass
            
            if text_from_pdf:
                request.session["text"] = text_from_pdf
            else:
                messages.error(request, "Invalid file format !!")
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
    image.save("media/folder_images/imagen.png")
    img="media/folder_images/imagen.png"
    return img


def success(image):
    text = pytesseract.image_to_string(Image.open(image))
    return text


# Convert images to text
def uploader(request):
    text_from_image = None
    if request.method == "POST":
        img = request.FILES["uploaded_img"]
        images = ImageUploader()
        images.image_to_convert = img
        images.save()
        
        file= settings.MEDIA_ROOT + '/' + str(img)
        file_extension = pathlib.Path(file).suffix
        try:
            if file_extension.endswith((".png", ".jpg", ".jpeg", ".webp", ".gif")):
                text_from_image = success(img)
        except:
            pass

        if text_from_image and img:
            request.session["text"] = text_from_image
            session_img=ImageUploader.objects.get(image_to_convert=images.image_to_convert)
            request.session["image_key"]=session_img.id
            
        else:
            messages.error(request, "Invalid file format!!")
            return redirect("uploader")

    context = {
        "text": text_from_image,
    }
    return render(request, "convert/upload.html", context)


@login_required(login_url="login")
def folders_list(request):
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
def documents_save(request, folder_slug=None):
    categories = None
    item = None
    text_from_image = None
    is_item_exist = None
    
    if folder_slug != None:
        categories = get_object_or_404(Folder, slug=folder_slug)
        item_list = Content.objects.filter(folder=categories).order_by('file_name')
       
        try:
            is_item_exist = request.session["text"]
        except:
            pass

        if request.method == "POST":
            file_name = request.POST["file_name"]
            item = Content()
            text_from_image = request.session["text"]
            item.folder_text = text_from_image
            item.folder = categories
            item.file_name = file_name
            item.slug = file_name
            item.save()
            try:
                if "text" in request.session:
                    del request.session["text"]
            except:
                pass
            
            messages.success(request, "Document saved successfully in "+ str(categories))
            return redirect('folders_list')
            
        # else:
        # 	item_list = Content.objects.filter(folder=categories)
    else:
        return redirect("folders_list")

    context = {
        "item": item,
        "text": text_from_image,
        "objects": item_list,
        "is_item_exist" : is_item_exist,
    }
    return render(request, "files/file_contents.html", context)


def file_path(request, folder_slug, file_slug):
    single_file = Content.objects.get(
        folder__slug=folder_slug, slug=file_slug
    )
    try:
        check = request.session["is_save"]
    except:
        check=None
    context = {
        "single_file": single_file,
        "check": check,
    }
    return render(request, "files/file_path.html", context)
