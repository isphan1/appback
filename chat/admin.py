from django.contrib.auth.models import User
from django.contrib import admin
from  chat.models import Profile,Message,RelationShip
# Register your models here.

admin.site.unregister(User)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username','is_staff']
    ordering =['-date_joined']

@admin.register(Profile)
class FriendAdmin(admin.ModelAdmin):
    list_display = ["id",'user','friend_list','avatar']

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['m_sender','m_reciver','msg','created_at']

@admin.register(RelationShip)
class RelationShipAdmin(admin.ModelAdmin):
    list_display = ['status_list','created_at']