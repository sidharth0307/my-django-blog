from django.shortcuts import render, get_object_or_404,redirect
from .models import Post
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import UserUpdateForm, ProfileUpdateForm

# Create your views here.
def home(request):
	posts = Post.objects.all()
	return render(request, 'blog/home.html',{'posts':posts})

def post_detail(request, pk):
	post = get_object_or_404(Post,pk=pk)
	return render(request,'blog/post_detail.html',{'post':post}) 

def register(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			messages.success(request, f'Account created for {username}!')
			return redirect('login')


	else:
		form = UserCreationForm()
	return render(request,'blog/register.html',{'form':form})


@login_required
def create_post(request):
	# Logic for creating a post
	pass


@login_required
def profile(request):
	if request.method == 'POST':
		u_form = UserUpdateForm(request.POST, instance=request.user)
		p_form = ProfileUpdateForm(request.POSTrequest.FILES, instance=request.user.profile)
		if u_form.is_valid() and p_form.is_valid():
			u_form.save()
			p_form.save()
			messages.success(request, f'Your account has been updated!')
			return redirect('profile')

		else:
			u_form = UserUpdateForm(instance=request.user)
			p_form = ProfileUpdateForm(instance=request.user.profile)


		context = {
			'u_form' : u_form,
			'p_form' : p_form
		}

		return render(request,'blog/profile.html',context)