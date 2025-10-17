from django import forms
from .models import User, Post, Response, CategorySubscription

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'category', 'image', 'video_url']

class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ['text']

class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = CategorySubscription
        fields = ['category']
