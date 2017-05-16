from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post, Entry


class RegisterForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ['author', 'slug']
        fields = '__all__'

class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = '__all__'

