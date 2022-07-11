from urllib.parse import uses_relative
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth import logout
def login(request):
    if request.method == 'POST':
        email  = request.POST['email'].replace(' ', '').lower()
        password = request.POST['password']
        user = auth.authenticate(username = email, password= password)


        if user:
            auth.login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid Credentials or User does not Exists")
            return redirect('register')
    return render(request, 'authorization/login.html', {})


def register(request):
    if request.method == 'POST':
        email  = request.POST['email'].replace(' ', '').lower()
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if not password1 == password2:
            messages.error(request, "Passwords do not match")
            return redirect('register')
        if User.objects.filter(email = email).exists():
            messages.error(request, "Email Already Exists")
            return redirect('register')

        user = User.objects.create_user(email=email, username = email, password = password1)
        user.save()

        auth.login(request, user)
        return redirect('home')

    return render(request, 'authorization/register.html', {})


def logout_request(request):
    logout(request)
    messages.info(request, "Logged Out Successfully")
    return redirect('home')