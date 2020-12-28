from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='profile')
    friends = models.ManyToManyField(User,related_name='friends')
    avatar = models.ImageField(default="avatar.png",upload_to="avatars/")

    def friend_list(self):
        return (",").join([str(f) for f in self.friends.all()])

    def __str__(self) -> str:
        return self.user.username

class Messages(models.Model):

    sender_p = models.ForeignKey(Profile,on_delete=models.CASCADE,related_name="user_m")
    reciver_p = models.ForeignKey(Profile,on_delete=models.CASCADE,related_name="friend_m")
    msg = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True,blank=True)

    def __str__(self) -> str:
        return self.msg