from django.urls import path
from . import views
from .views import post_detail,like_post,dislike_post,search_posts
from .views import PostEditView,PostDeleteView

urlpatterns = [
	path('', views.home,name='home'),
	path('post/<int:pk>/', views.post_detail, name='post_detail'),
	path('post/new/', views.create_post, name='post-create'),
	path('profile/<str:username>/', views.profile,name='profile'),
	path('create/',views.create_post,name='create_post',),
	path('post/<int:pk>/like/',views.like_post, name='like_post'),
	path('post/<int:pk>/dislike/',views.dislike_post, name='dislike_post'),
	path('search/',search_posts,name='search_posts'),
	path('post/<int:pk>/edit/', PostEditView.as_view(),name='post_edit'),
	path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
	]