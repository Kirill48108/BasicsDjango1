from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.views.generic import CreateView,FormView,UpdateView

from  .forms import RegistrationForm,EmailAuthenticationForm,ProfileForm
from  django.contrib.auth import get_user_model


User = get_user_model()

class RegisterView(CreateView):
    form_class = RegistrationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('catalog:products')


    def form_valid(self, form):
        response = super().form_valid(form)
        users = self.object
        login(self.request, users)
        send_mail(
            subject='Добро пожаловать!',
            message='Спасибо за регистрацию в нашем магазине.',
            from_email=None,
            recipient_list=[users.email],
            fail_silently=True,
        )
        messages.success(self.request,'Вы успешно зарегистрированы.')
        return response


class LoginView(FormView):
    form_class = EmailAuthenticationForm
    template_name = 'users/login.html'


    def get_success_url(self):
        next_url = self.request.GET.get('next')
        return next_url if next_url else reverse_lazy('catalog:products')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


    def form_valid(self, form):
        user = form.get_user()
        login(self.request,user)
        messages.success(self.request,'Вы успешно вошли.')
        return super().form_valid(form)


class LogoutCBV(LogoutView):
    next_page = reverse_lazy('catalog:home')
    http_method_names = ['get', 'post', 'head', 'options']
    def get(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class ProfileUpdateView(LoginRequiredMixin,UpdateView):
    model = User
    form_class = ProfileForm
    template_name = 'users/profile.html'
    success_url = reverse_lazy('users:profile')

    def get_object(self,qeryset=None):
        return self.request.user


    def form_valid(self, form):
        messages.success(self.request,'Профиль обновлен.')
        return super().form_valid(form)