from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile,RelationShip

@receiver(post_save,sender=User)
def post_save_create_profile(sender,instance,created,**kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save,sender=RelationShip)
def post_save_create_relationship(sender,instance,created,**kwargs):

    sender_ = instance.sender
    reciver_ = instance.reciver

    if instance.status == 'accpeted':
        print(instance)
        sender_.friends.add(reciver_.user)
        reciver_.friends.add(sender_.user)
        sender_.save()
        reciver_.save()