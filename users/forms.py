from django import forms
from django.contrib.auth import get_user_model, authenticate

User = get_user_model()

class RegistrationForm(forms.ModelForm):
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email',)

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('Пользователь с таким email уже существует.')
        return email

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get('password1')
        p2 = cleaned.get('password2')
        if p1 and p2 and p1 != p2:
            self.add_error('password2', 'Пароли не совпадают.')
        return cleaned

    def save(self, commit=True):
        email = self.cleaned_data['email'].lower()
        user = User(email=email)
        # генерируем username из email для совместимости с админкой
        base = email.split('@')[0][:150] or 'user'
        candidate = base
        i = 1
        while User.objects.filter(username=candidate).exists():
            suffix = f'_{i}'
            candidate = (base[:150 - len(suffix)]) + suffix
            i += 1
        user.username = candidate
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

class EmailAuthenticationForm(forms.Form):
    email = forms.EmailField(label='Email')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned = super().clean()
        email = cleaned.get('email')
        password = cleaned.get('password')
        if email and password:
            # так как USERNAME_FIELD = 'email', передаем username=email
            self.user_cache = authenticate(self.request, username=email, password=password)
            if self.user_cache is None:
                raise forms.ValidationError('Неверный email или пароль.')
            if not self.user_cache.is_active:
                raise forms.ValidationError('Учетная запись отключена.')
        return cleaned

    def get_user(self):
        return self.user_cache

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('avatar', 'phone', 'country')
