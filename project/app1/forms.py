from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
import re
from django import forms
from .models import Server ,Channel
from .models import FriendRequest

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Set Password'}))
    class Meta:
        model = User
        fields = ['email', 'username', 'password',]
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'Enter your Email'}),
            'username': forms.TextInput(attrs={'placeholder': 'Set your Username'}),
        }
    def clean_email(self):
        email = self.cleaned_data.get('email')
        email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        if not re.match(email_regex, email):
            raise ValidationError('Enter a valid email address.')
        if User.objects.filter(email=email).exists():
            raise ValidationError('Email address already in use.')
        return email
    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise ValidationError('Password must be at least 8 characters long.')
        if not re.search(r"[A-Z]", password):
            raise ValidationError('Password must contain at least one uppercase letter.')
        if not re.search(r"[a-z]", password):
            raise ValidationError('Password must contain at least one lowercase letter.')
        if not re.search(r"[0-9]", password):
            raise ValidationError('Password must contain at least one digit.')
        if not re.search(r"[@$!%*?&]", password):
            raise ValidationError('Password must contain at least one special character.')
        return password
class ServerForm(forms.ModelForm):
    class Meta:
        model = Server
        fields = ['name', 'description','public']
    
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if Server.objects.filter(name=name).exists():
            raise forms.ValidationError("A server with this name already exists.")
        return name
class ChannelForm(forms.ModelForm):
    class Meta:
        model = Channel
        fields = ['name', 'channel_type']

class FriendRequestForm(forms.ModelForm):
    class Meta:
        model = FriendRequest
        fields = []  
class SearchForm(forms.Form):
    username = forms.CharField(max_length=150, required=True, label='Search for a user')