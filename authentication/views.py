from django.shortcuts import render, redirect
from django.views.generic import CreateView, View
from django.contrib.auth.models import User
from django.contrib import messages
from skin_cancer.models import SkinUser
from django.contrib.auth import login as auth_login, logout
from django.conf import settings
import os



class SignUpView(CreateView):
    model = User
    template_name = 'authentication/sign-up.html'

    def post(self, request):
        if request.POST:
            username = self.request.POST['username']
            password1 = self.request.POST['password1']
            password2 = self.request.POST['password2']
            email = self.request.POST['email']
            first_name = self.request.POST['fname']
            last_name = self.request.POST['lname']
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exist')
                return redirect('sign-up')
            elif password1!=password2:
                messages.error(request, "Password didn't match")
                return redirect('sign-up')
            elif password1==password2 and len(password1)<8:
                messages.error(request, "Password mus be 8 characters")
                return redirect('sign-up')
            
            gender = self.request.POST['gender']
            
            user = User.objects.create(first_name=first_name, last_name=last_name, username=username, email=email, password=password1)
            
            p_user = SkinUser.objects.create(user=user, gender=gender)
            p_user.save()
            auth_login(self.request, user)
            return redirect("home")
        
        return redirect('sign-up')

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
    


class SignIn(View):
    template_name = 'authentication/sign-in.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        if request.POST:
            username = self.request.POST['username']
            password = self.request.POST['password']
            
            if User.objects.filter(username=username, password=password).exists():
                user = User.objects.get(username=username, password=password)
                auth_login(request, user)
                messages.success(request, 'Sign in Successfully!')
                return redirect('home')
            else:
                messages.error(request, 'Bad Credential!')

        return render(request, self.template_name)



class SignOut(View):
    def get(self, request):
        logout(request)
        messages.success(request, 'Sign out Successfully!')
        return redirect('sign-in')
    