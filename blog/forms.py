from django import forms
from django.contrib.auth.models import User
from .models import Profile
from .models import Post
from.models import Comment
class UserUpdateForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ['username','email']

class ProfileUpdateForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ['image']


class PostForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = ['title','content',]

class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ['content']

class ProfileForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ['bio','image'] 