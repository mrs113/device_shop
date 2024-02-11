from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView, PasswordResetView, \
    PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import path, reverse_lazy
# from .views import *
from . import views

urlpatterns = [
    path('login', views.Login.as_view(), name='login'),
    path('log_out', views.log_out, name='log_out'),
    path('register', views.register, name='register'),
    path('profile', views.Profile.as_view(), name='profile'),
    path('password-change', views.UserChangePasswordView.as_view(), name='password_change'),
    path('password-change/done/', PasswordChangeDoneView.as_view(template_name='users/password_done.html'), name='password_change_done'),
    path('password-reset/', PasswordResetView.as_view(
        template_name='users/password_reset_form.html',
        success_url=reverse_lazy('users:password_reset_done'),
        email_template_name='users/password_reset_email.html'), name='password_reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(template_name="users/password_reset_done.html"), name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(
        template_name="users/password_reset_confirm.html",
        success_url=reverse_lazy("users:password_reset_complete")), name='password_reset_confirm'),
    path('password-reset/complete/', PasswordResetCompleteView.as_view(
        template_name='users/password_reset_complete.html'), name='password_reset_complete'),
    path('user_orders', views.user_orders, name='user_orders'),
    path('user_orders_button', views.user_orders_button, name='user_orders_button'),
]
