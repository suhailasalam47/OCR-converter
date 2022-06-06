from django.shortcuts import redirect, render
from django.contrib.auth.models import User, auth
from django.contrib import messages

# Create your views here.
def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1==password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, "username taken")
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.error(request, "email taken")
                return redirect('register')
            else:        
                user = User.objects.create_user(first_name=first_name,username=username,email=email,password=password1)
                user.save()
                return redirect('/')
        else:
            return redirect('register')        

    else:    
        return render(request, 'register.html')

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.error(request, "Invalid credentials")    
            return redirect('login')

    else:    
        return render(request, 'login.html')        
    