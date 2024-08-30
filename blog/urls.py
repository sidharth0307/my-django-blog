from django.urls import path
from . import views

urlpatterns = [
	path('', views.home,name='home'),
	path('post/<int:pk>/', views.post_detail, name='post_detail'),
	path('post/new/', views.create_post, name='post-create'),
	path('post/new/', views.create_post,name='post-create'),
	]