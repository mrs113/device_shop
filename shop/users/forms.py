from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput)
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)

    class Meta:
        model = get_user_model()
        # fields = ['username', 'password']


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин*', widget=forms.TextInput)
    password1 = forms.CharField(label='Пароль*', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повторите пароль*', widget=forms.PasswordInput)
    email = forms.EmailField(label='E-mAil*', widget=forms.EmailInput)

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
        }

    # def clean_password2(self):
    #     cd = self.cleaned_data
    #     if cd['password'] != cd['password2']:
    #         raise forms.ValidationError('Пароли не совпадают!')
    #     return cd['password']

    def clean_email(self):
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError('Пользователь с таким email уже существует!')
        return email


class ProfileUserForm(forms.ModelForm):
    username = forms.CharField(disabled=True, label='Логин*', widget=forms.TextInput(attrs={'class': 'profile_input'}))
    email = forms.EmailField(disabled=True, label='E-mAil*', widget=forms.EmailInput(attrs={'class': 'profile_input'}))

    class Meta:
        model = get_user_model()
        fields = ['image', 'username', 'email', 'first_name', 'last_name']
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
        }

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'profile_input'}),
            'last_name': forms.TextInput(attrs={'class': 'profile_input'})
        }


class UserPasswordChange(PasswordChangeForm):
    old_password = forms.CharField(label='Старый пароль', widget=forms.PasswordInput(attrs={'class': 'profile_input'}))
    new_password1 = forms.CharField(label='Новый пароль', widget=forms.PasswordInput(attrs={'class': 'profile_input'}))
    new_password2 = forms.CharField(label='Подтвердите пароль', widget=forms.PasswordInput(attrs={'class': 'profile_input'}))
