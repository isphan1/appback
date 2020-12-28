from django.core.checks import messages
from django.http.response import HttpResponse
from django.shortcuts import render
from chat.models import Profile,Messages
# Create your views here.

def index(request):

    friends = Profile.objects.filter(user_id=2)
    list = []

    for c in friends:
        m = []

        msg1 = Messages.objects.filter(user_m=2).filter(friend_m=c.friend_id.id).order_by('created_at')
        msg2 = Messages.objects.filter(user_m=c.friend_id.id).filter(friend_m=2).order_by('created_at')

        for x in msg1:
                m.append(x)
        for x in msg2:
                m.append(x)
            
        def myFunc(e):
            return e.created_at

        m.sort(key=myFunc)

        list.append(m)
            

    return render(request,'index.html',{'list':list})