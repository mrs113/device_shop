from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordResetView
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView

from .forms import LoginUserForm, RegisterUserForm, ProfileUserForm, UserPasswordChange
from carts.models import Cart
from orders.models import OrderItem


# def login_user(request):
#     if request.method == 'POST':
#         form = LoginUserForm(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#             user = authenticate(request, username=cd['username'], password=cd['password'])
#             if user and user.is_active:
#                 login(request, user)
#                 return HttpResponseRedirect(reverse('products:home'))
#     else:
#         form = LoginUser()
#     return render(request, 'users/login.html', {'form': form})


class Login(LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'
    extra_context = {'title': 'Авторизация'}

    # def get_success_url(self):
    #     return reverse_lazy('products:home')


def log_out(request):
    logout(request)
    messages.success(request, 'Вы вышли из аккаунта:(')
    return HttpResponseRedirect(reverse('products:home'))


def register(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()

            session_key = request.session.session_key

            login(request, user)

            if session_key:
                Cart.objects.filter(session_key=session_key).update(user=user)

            messages.success(request, f'{user.username}, вы успешно зарегестрированы!')
            return HttpResponseRedirect(reverse('products:home'))
    else:
        form = RegisterUserForm()
    return render(request, 'users/register.html', {'form': form})


class Profile(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = ProfileUserForm
    template_name = 'users/profile.html'
    extra_context = {'title': 'Профиль', 'default_image': settings.DEFAULT_USER_IMAGE}

    def get_success_url(self):
        return reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super(Profile, self).get_context_data(**kwargs)
        context['order_items'] = OrderItem.objects.filter(user=self.request.user)
        return context


class UserChangePasswordView(PasswordChangeView):
    form_class = UserPasswordChange
    success_url = reverse_lazy('users:password_change_done')
    template_name = 'users/password_change_form.html'
    extra_context = {'title': 'Изменение пароля'}


# class UserPasswordReset(PasswordResetView):
#     template_name = 'users/password_reset_form.html'
#     success_url = reverse_lazy('users:password_reset_done')
#     email_template_name = 'users/password_reset_email.html'


def user_orders(request):
    order_items = OrderItem.objects.filter(user=request.user)
    return render(request, 'orders/includes/order_items.html', {'order_items': order_items})


def user_orders_button(request):
    order_items = OrderItem.objects.filter(user=request.user)
    return render(request, 'users/user_orders.html', {'order_items': order_items})
