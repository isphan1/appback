from django.core.checks import messages
from django.http.response import HttpResponse
from django.shortcuts import render
from chat.models import Profile,Message
# Create your views here.

def index(request):

    friends = Profile.objects.filter(user_id=2)    
    return render(request,'index.html',{'list':friends})