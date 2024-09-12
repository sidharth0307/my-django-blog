from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Post(models.Model):
	title = models.CharField(max_length=100)
	content = models.TextField()
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.title

	
class Profile(models.Model):
	user = models.OneToOneField(User,on_delete=models.CASCADE)
	image = models.ImageField(default='default.jpg', upload_to='profile_pics')
	bio = models.TextField(blank=True)

	def __str__(self):
		return f'{self.user.username} Profile'

class Comment(models.Model):
	post = models.ForeignKey(Post, related_name="comments",on_delete=models.CASCADE)
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	content = models.TextField()
	date_posted = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f'Comment by {self.author} on {self.post}'


class Like(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	post = models.ForeignKey(Post, on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		unique_together = ('user','post')

	def __str__(self):
		return f"{self.user.username} likes {self.post.title}"

class Dislike(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	post = models.ForeignKey(Post, on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		unique_together = ('user','post')


