from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    bio = models.TextField(blank=True)  # bio can be blank if user doesn't want to add one
    location = models.CharField(max_length=100)
    occupation = models.CharField(max_length=100)
    profile_picture = models.ImageField(upload_to='profile_pictures', blank=True, default='default_profile_picture.jpg')
    friends = models.ManyToManyField("self", blank=True)

    def is_friends(self, user):
        return user in self.friends.all()



class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='posts/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class FriendRequest(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend_request_sent')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend_request_received')
    timestamp = models.DateTimeField(auto_now_add=True)  # set timestamp when friend request was sent

    def __str__(self):
        return f'{self.sender.username} wants to be friends with {self.receiver.username}'
