from django.shortcuts import render
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm,AuthenticationForm
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView,PasswordChangeDoneView,LoginView

class RegisterView(CreateView):
    form_class =UserCreationForm
    template_name = "registration/register.html" 
    success_url = reverse_lazy('login') 

class UserLogin(LoginView):
    form_class = AuthenticationForm
    template_name = 'registration/login.html'

class ChangePassword(PasswordChangeView):
    form_class = PasswordChangeForm
    template_name =  "registration/password_change_form.html" 


class PasswordChanged(PasswordChangeDoneView):
    template_name =  "registration/password_change_done.html" 
    