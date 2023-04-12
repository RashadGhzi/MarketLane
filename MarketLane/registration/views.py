from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetDoneView, PasswordChangeDoneView, PasswordChangeView, PasswordResetCompleteView, PasswordResetConfirmView
from .forms import UserRegistrationForm
from django.views.generic import FormView, View
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

class RegistrationView(FormView):
    form_class = UserRegistrationForm
    template_name = 'registration/user_registration.html'
    success_url = reverse_lazy('user_login') 

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
    
class LogInView(LoginView):
    template_name = 'registration/login.html'

    def form_invalid(self, form):
        messages.error(self.request, 'enter valid username and password')
        return super().form_invalid(form)

class LogOutView(LoginRequiredMixin,View):
    login_url = reverse_lazy('user_login')
    def dispatch(self, request, *args, **kwargs):
        logout(request)
        messages.success(self.request,'logout successfully')
        return redirect('user_login')
    
class PasswordReset(PasswordResetView):
    template_name = 'registration/password_reset.html'
    success_url = reverse_lazy('password_reset_done')

class PasswordResetDone(PasswordResetDoneView):
    login_url = reverse_lazy('user_login')
    template_name = 'registration/password_reset_done_view.html'

class PasswordResetConfirm(PasswordResetConfirmView):
    template_name = 'registration/password_reset_confirm_view.html'

class PasswordResetComplete(PasswordResetCompleteView):
    template_name = 'registration/password_reset_complete_view.html'

class PasswordChange(LoginRequiredMixin,PasswordChangeView):
    login_url = reverse_lazy('user_login')
    template_name = 'registration/password_change_view.html'
    success_url = reverse_lazy('password_change_done')

class PasswordChangeDone(LoginRequiredMixin,PasswordChangeDoneView):
    login_url = reverse_lazy('user_login')
    template_name = 'registration/password_change_done_view.html'