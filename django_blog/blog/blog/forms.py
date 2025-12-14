from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from taggit.forms import TagWidget   # <-- import TagWidget
from .models import Post


class RegisterForm(UserCreationForm):
    """Custom registration form extending Django's UserCreationForm with email validation."""

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'placeholder': 'Email address',
            'class': 'form-control'
        }),
        help_text="Required. Enter a valid email address."
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={
                'placeholder': 'Username',
                'class': 'form-control'
            }),
            'password1': forms.PasswordInput(attrs={
                'placeholder': 'Password',
                'class': 'form-control'
            }),
            'password2': forms.PasswordInput(attrs={
                'placeholder': 'Confirm password',
                'class': 'form-control'
            }),
        }
        help_texts = {
            'username': None,
            'password1': "Your password must be at least 8 characters long.",
            'password2': "Enter the same password again for verification.",
        }

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('This email is already registered. Please use a different one.')
        return email

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError('This username is already taken. Please choose another.')
        return username


class ProfileForm(forms.ModelForm):
    """Form for updating user profile information."""

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')
        widgets = {
            'username': forms.TextInput(attrs={
                'readonly': 'readonly',
                'class': 'form-control'
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Email',
                'class': 'form-control'
            }),
            'first_name': forms.TextInput(attrs={
                'placeholder': 'First name',
                'class': 'form-control'
            }),
            'last_name': forms.TextInput(attrs={
                'placeholder': 'Last name',
                'class': 'form-control'
            }),
        }
        help_texts = {
            'username': 'Your username cannot be changed.',
        }

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        if User.objects.filter(email__iexact=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('This email is already in use by another account.')
        return email


class PostForm(forms.ModelForm):
    """Form for creating and updating blog posts with tags."""

    class Meta:
        model = Post
        fields = ('title', 'content', 'tags')  # include tags directly
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Post title',
                'class': 'form-control'
            }),
            'content': forms.Textarea(attrs={
                'placeholder': 'Write your content here...',
                'class': 'form-control',
                'rows': 8
            }),
            'tags': TagWidget(attrs={
                'placeholder': 'Comma-separated tags (e.g. django, web, tutorial)',
                'class': 'form-control'
            }),
        }
