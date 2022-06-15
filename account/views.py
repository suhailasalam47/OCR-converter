from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth

from .models import Account
from .forms import RegistrationForm, UserForm
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from project import settings
from django.contrib.auth.decorators import login_required


# Create your views here.
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password1 = form.cleaned_data['password']
            # password2 = request.POST['password2']

            user = Account.objects.create_user(first_name=first_name, username=username,email=email, password=password1)
            user.save()

            #USER ACTIVATION
            current_site = get_current_site(request)
            mail_subject = 'Please activate your account'
            message = render_to_string('email_verification.html',{
                'user':user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })

            to_email = email
            email_from = settings.EMAIL_HOST_USER
            send_email = EmailMessage(mail_subject, message, email_from, to=[to_email],)
            send_email.send()

            # messages.success(request, "Thank you for registering with us.We have sent you a verification email to your email address. Please verify it.")

            return redirect('/account/login/?command=verification&email='+email)
    else:
        form = RegistrationForm()    
    context = {
        'reg_form': form,
        }
    return render(request, 'register.html', context)       
        

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = auth.authenticate(email=email, password=password)
        if user is not None:
            auth.login(request, user)
            print("login succesful")
            return redirect('/')
        else:
            messages.error(request, "Invalid credentials")    
            return redirect('login')

    return render(request, 'login.html') 

def activate(request, uidb64, token):
    try:
        uid =urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save() 
        messages.success(request,  "Congratulations! Your account has been activated.")
        return redirect('login')                 
    else:
        messages.error(request, "Invalid activation link")
        return redirect('register')


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)

            current_site = get_current_site(request)
            mail_subject = 'Reset your Password'
            message = render_to_string('password/reset_password_email.html',{
                'user':user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })

            to_email = email
            email_from = settings.EMAIL_HOST_USER
            send_email = EmailMessage(mail_subject, message, email_from, to=[to_email],)
            send_email.send()

            messages.success(request, "Password reset email has been sent to your email address")
            return redirect('login')

        else:
            messages.error(request, "Account does not exist!") 
            return redirect('forgot_password')   

    return render(request, 'password/forgot_password.html')    


def resetpassword_validate(request, uidb64, token):
    try:
        uid =urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, "Please reset your password")
        return redirect('reset_password')
    else:
        messages.error(request, "This link has been expired!") 
        return redirect('login')   


def reset_password(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, "Password reset successful")
            return redirect('login')

        else:
            messages.error(request, "Password do not match!")
            return redirect('reset_password')   
    else:         
        return render(request, 'password/reset_password.html')        


def logout(request):
    auth.logout(request)
    return redirect('/')

@login_required(login_url='login')
def profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, "Your profile has been updated")
            return redirect('profile')
    else:
        user_form = UserForm(instance=request.user)  
    context = {
        'user_form': user_form,
    }      
    return render(request, 'profile.html', context)


@login_required(login_url='login')
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        user = Account.objects.get(email__exact=request.user.email)
        
        if new_password == confirm_password:
            success = user.check_password(current_password)
            if success:
                user.set_password(new_password)
                user.save()
                messages.success(request, "Password changed successfully")
                return redirect('profile')
            else:
                messages.error(request, "Please enter valid current password") 
                return redirect('change_password')
        else:
            messages.error(request, "Password does not match")
            return redirect('change_password')           

    return render(request, 'password/change_password.html')    