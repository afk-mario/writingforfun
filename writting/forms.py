from django import forms
from .models import Post, Entry

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ['author', 'slug']
        fields = '__all__'

class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = '__all__'

