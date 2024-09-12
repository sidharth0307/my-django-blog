from django.shortcuts import render, get_object_or_404,redirect
from .models import Post, Comment, Like, Dislike
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.views import LoginView
from .forms import PostForm
from .forms import CommentForm
from .forms import PostForm
from django.urls import reverse_lazy
from django.views.generic import UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator
from django.conf import settings
import requests

# Create your views here.
def home(request):
	posts = Post.objects.all().order_by('-created_at')
	news_articles = fetch_news()
	paginator = Paginator(posts, 5)

	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)

	context = {
		'page_obj': page_obj,
		'posts':posts,
		'news_articles': news_articles,
	}
	return render(request, 'blog/home.html', context)

def post_detail(request, pk):
	post = get_object_or_404(Post,pk=pk)
	comments = Comment.objects.filter(post=post)

	user_has_liked = False
	user_has_disliked = False
	if request.user.is_authenticated:
		user_has_liked = post.like_set.filter(user = request.user).exists() 
		user_has_disliked = Dislike.objects.filter(user=request.user, post=post).exists()

	if request.method == 'POST':
		form = CommentForm(request.POST)
		if form.is_valid():
			comment = form.save(commit=False)
			comment.post = post
			comment.author = request.user
			comment.save()
			return redirect('post_detail',pk=post.pk)
	else:
		form = CommentForm()

	like_count = Like.objects.filter(post=post).count()
	dislike_count = Dislike.objects.filter(post=post).count()

	return render(request,'blog/post_detail.html',{'post':post,'comments':comments,'form':form,'user_has_liked':user_has_liked, 'user_has_disliked': user_has_disliked,'like_count':like_count,'dislike_count':dislike_count,}) 

def register(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			messages.success(request, f'Account created for {username}! You can now log in.')
			return redirect('login')


	else:
		form = UserCreationForm()
	return render(request,'blog/register.html',{'form':form})


@login_required
def create_post(request):
	# Logic for creating a post
	pass


@login_required
def profile(request,username=None):
	user =get_object_or_404(User, username=username) if username else request.user 
	if request.method == 'POST':
		u_form = UserUpdateForm(request.POST, instance=user)
		p_form = ProfileUpdateForm(request.POST,request.FILES, instance=user.profile)
		if u_form.is_valid() and p_form.is_valid():
			u_form.save()
			p_form.save()
			messages.success(request, 'Your account has been updated!')
			return redirect('profile',username=user.username)

	else:
		u_form = UserUpdateForm(instance=user)
		p_form = ProfileUpdateForm(instance=user.profile)
		

	posts = Post.objects.filter(author=user)

	context = {
		'u_form' : u_form,
		'p_form' : p_form,
		'posts' : posts,
		'user': user,
	}

	return render(request,'blog/profile.html',context)



class CustomLoginView(LoginView):
	template_name = 'blog/login.html'

	def form_valid(self,form):
		messages.success(self.request, f'Welcome back, {self.request.user.username}!')
		return super().form_valid(form)


@login_required
def create_post(request):
	if request.method == 'POST':
		form = PostForm(request.POST)
		if form.is_valid():
			post = form.save(commit=False)
			post.author = request.user
			post.save()
			return redirect('home')

	else:
		form =PostForm()
	return render(request,'blog/create_post.html',{'form':form})

@login_required
def like_post(request,pk):
	post = get_object_or_404(Post,pk=pk)
	try:
		like = Like.objects.get(user=request.user, post=post)
		like.delete()
	except Like.DoesNotExist:
		Like.objects.create(user=request.user, post=post)
	return redirect('post_detail', pk=pk)

@login_required
def dislike_post(request, pk):
	if Dislike.objects.filter(user=request.user, post=post).exists():
		Dislike.objects.filter(user=request.user,post=post).delete()
	else:
		Dislike.objects.create(user=request.user, post=post)

	return redirect('post_detail',pk=pk)


def search_posts(request):
	query = request.GET.get('q','')
	if query:
		posts = Post.objects.filter(title__icontains=query)
	else:
		posts = Post.objects.none()

	return render(request,'blog/search_results.html',{'posts':posts,'query':query})


class PostEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Post
	fields = ['title','content']
	template_name = 'blog/post_edit.html'
	context_object_name = 'post'


	def test_func(self):
		post = self.get_object()
		return self.request.user == post.author

	def get_success_url(self):
		return reverse_lazy('post_detail', kwargs={'pk': self.object.pk})


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Post
	template_name = 'blog/post_confirm_delete.html'
	context_object_name = 'post'
	success_url = reverse_lazy('home')

	def test_func(self):
		post = self.get_object()
		return self.request.user == post.author


def fetch_news():
	url = 'https://newsapi.org/v2/top-headlines'
	params = {

		'apiKey': settings.NEWS_API_KEY,
		'country': 'us',
		'category': 'general'
		}
	response = requests.get(url, params=params)

	if response.status_code ==200:
		return response.json().get('articles', [])
	else:
		return []
