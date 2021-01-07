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

class Message(models.Model):

    m_sender = models.ForeignKey(Profile,on_delete=models.CASCADE,related_name="m_sender")
    m_reciver = models.ForeignKey(Profile,on_delete=models.CASCADE,related_name="m_reciver")
    msg = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True,blank=True)

    def __str__(self) -> str:
        return self.msg

class RelationShip(models.Model):

    STATUS_CHOICE = (
        ('send',"send"),
        ('accpeted',"accpeted"),
    )

    sender = models.ForeignKey(Profile,on_delete=models.CASCADE,related_name="sender")
    reciver = models.ForeignKey(Profile,on_delete=models.CASCADE,related_name="reciver")
    status = models.CharField(max_length=10,choices=STATUS_CHOICE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def status_list(self) -> str:
        return f"{self.sender}-{self.reciver}-{self.status}"

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    notes = models.TextField()
    category = models.ForeignKey(
        Category, related_name="ingredients", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name