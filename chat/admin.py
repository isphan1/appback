from django.contrib.auth.models import User
from django.contrib import admin
from  chat.models import Profile,Messages
# Register your models here.

admin.site.unregister(User)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id','username','is_staff']
    ordering =['-date_joined']

@admin.register(Profile)
class FriendAdmin(admin.ModelAdmin):
    list_display = ['user','friend_list','avatar']

@admin.register(Messages)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['sender_p','reciver_p','msg','created_at']