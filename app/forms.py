from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from app.models import Stories,Post,Comment

class SigninForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100)
    widgets = {
            'username': forms.TextInput(attrs={'class':'form-control','placeholder':'username'}),
            'password': forms.TextInput(attrs={'class':'form-control','placeholder':'password'}),
        }

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','username','password1','password2','email','bio','profile_picture']
        widgets = {
            'first_name': forms.TextInput(attrs={'class':'form-control'}),
            'last_name': forms.TextInput(attrs={'class':'form-control'}),
            'username': forms.TextInput(attrs={'class':'form-control'}),
            'password1': forms.TextInput(attrs={'class':'form-control'}),
            'password2': forms.TextInput(attrs={'class':'form-control'}),
            'email': forms.EmailInput(attrs={'class':'form-control'}),
            'bio': forms.TextInput(attrs={'class':'form-control'}),
            
        }


class AddPostForm(forms.ModelForm):
    class Meta:
        model=Post
        fields=['image','caption']
        widgets = {
    
            'caption': forms.TextInput(attrs={'class':'form-control'}),
        }


class AddStoryForm(forms.ModelForm):
    class Meta:
        model=Stories
        fields=['image']

class CommentForm(forms.ModelForm):
    class Meta:
        model=Comment
        fields=['content']

