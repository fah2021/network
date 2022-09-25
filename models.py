
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass
  
class Posts(models.Model):
    message = models.CharField(max_length=500)
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="user")
    timestamp = models.DateTimeField(auto_now_add=True, blank=True)
    likes=models.ManyToManyField(User, related_name="user_likes")
    total_likes= models.IntegerField(default=0)

    class Meta:
        ordering = ["-timestamp"]


    def serialize(self):
        return {
            "id": self.id,
            "message": self.message,
            "user": self.user.username,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
        
        }

    def __str__(self):
       return self.user

     
class Follow(models.Model):
   follower = models.ForeignKey(User,on_delete=models.CASCADE,related_name="follower")
   user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="following")
   
   def serialize(self,user):
        return {
            "post_owner": self.user.id,
            "profile_username": self.user.username,
            "follower": self.follower.count(),
            "following": self.user.follower.count(),
            "following": not user.is_anonymous and self in user.get_followed_profiles.all(),
            "follow_available": (not user.is_anonymous) and self.user != user
            
        }

   def __str__(self):
       return self.user

   
