from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views import View


def index(request):
    return render(request, "users/index.html")


class SignUpView(View):
    def get(self, request):
        return render(request, "users/signup.html")

    def post(self, request):
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        new_user = User.objects.create_user(username, email, password)

        if new_user is None:
            return render(request, "users/signup.html")
        else:
            new_user.save()
            messages.success(request, "Kaydoldun.")
            return redirect('index')


class SignInView(View):
    def get(self, request):
        return render(request, "users/signin.html")

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Girdin.")
            return redirect('index')
        else:
            messages.error(request, "Salak.")
            return redirect('/index')


class SignOutView(View):
    def get(self, request):
        logout(request)
        return redirect('index')
