from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Post(models.Model):
    user = models.ForeignKey(User,on_delete = models.CASCADE)
    image = models.ImageField(upload_to='media')
    caption = models.CharField(max_length = 200,null = True)
    likes = models.ManyToManyField(User, related_name='postlikes', blank=True)
    comments = models.ForeignKey('Comment',on_delete = models.CASCADE, related_name = 'postcomment',blank = True,null = True)
    def number_of_likes(self):
        return self.likes.count()

class Stories(models.Model):
    user = models.ForeignKey(User,on_delete = models.CASCADE)
    image = models.ImageField(upload_to='media')

class Message(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add = True)
    def __str__(self):
        return f'{self.user.username}-{self.timestamp}'
    
def default_profile_picture():
    return 'media/user.png'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE,primary_key = True)
    profile_picture = models.ImageField(upload_to='media',default=default_profile_picture,null=True,blank=True) #set default dp
    bio = models.CharField(max_length=200,null = True,blank = True)



class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField()

class DirectMessage(models.Model):
    sender = models.ForeignKey(User, on_delete = models.CASCADE,related_name = 'sender')
    reciever = models.ForeignKey(User, on_delete = models.CASCADE,related_name = 'reciever')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add = True)
   
    
    