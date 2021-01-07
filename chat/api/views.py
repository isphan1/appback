from django.core.exceptions import ValidationError
from django.core.serializers import serialize
from django.db.models import Q
from rest_framework import viewsets
import rest_framework
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ProfileSerializers, MessageSerializers,UserSerializer
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin
from chat.models import Message, Profile
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly
import json
import random
import string 

url = "http://127.0.0.1:8000/media/"
# url = "http://wbclone.herokuapp.com/media/"

class UserCreateView(CreateAPIView,CreateModelMixin):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def post(self,request,*args,**kwargs):
        return self.create(request,*args,**kwargs)


class LoginUser(viewsets.ViewSet):

    def login(self,request):
        username = self.request.data['username']

        if username:
            
            user = authenticate(username=username,password="jnj")

            if user:
                list = {"username":user.username,"id":user.id}
                return Response(list)

            else:
                return Response({"msg":'Incorrect username or password. please try again !'},status=401)

class CreateNewMessage(viewsets.ViewSet):
    
    def list(self,request):

        s = Profile.objects.get(user__username=self.request.data['s_name'])
        r = Profile.objects.get(user__username=self.request.data['r_name'])

        newMsg = Message.objects.create(m_sender=s,m_reciver=r,msg=self.request.data['msg'])

        if newMsg:
            return Response({
                "id": newMsg.id,
                "createdAt": newMsg.created_at,
                "content": newMsg.msg,
                "user": {
                    "id": "u1",
                    "name": self.request.data['s_name']
                }
            })

        return Response({"msg":"Something went wrong !"})    
# {
# "s_name":"Alpha",
# "r_name":"Alen",
# }

#
##
###

class UserProfile(viewsets.ViewSet):
    
    def list(self,request):

        id = self.request.data['id']
        
        u = Profile.objects.get(id=id)

        def user(x):
            
            room = ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(10))
            return [
                    {"id":'u1' ,"name":u.user.username,"imageUri":"{}{}".format(url,u.avatar),"room":room},
                    {"id":'u{}'.format(x.profile.id) ,"name":x.profile.user.username,"imageUri":"{}{}".format(url,x.profile.avatar),"room":room},
                ]


        friends = [u for u in u.friends.all()]            
        list = []
        icd = 1
        for f in friends:
            m = []
            msg1 = Message.objects.filter(m_sender=id).filter(m_reciver=f.profile.id).values()
            msg2 = Message.objects.filter(m_sender=f.profile.id).filter(m_reciver=id).values()

            for x in msg1:
                    m.append({'id':x['id'],'createdAt':x['created_at'],'content':x['msg']})
            for x in msg2:
                    m.append({'id':x['id'],'createdAt':x['created_at'],'content':x['msg']})
            
            def myFunc(e):
                return e['createdAt']

            m.sort(key=myFunc)

            list.append( {
                "id":icd,
                "users":user(f),
                "lastMessage": m.pop() if len(m) >0 else m
            })

            icd = icd + 1

        return Response(list)
    
class UserMessage(viewsets.ViewSet):
    # serializer_class = Messageerializers

    def list(self,request):

        id_s = self.request.data['s_name']
        id_r = self.request.data['r_name']

        s = Profile.objects.get(user__username=id_s)
        r = Profile.objects.get(user__username=id_r)

        def user(x):
            
            p = User.objects.get(id=x.id)

            return {'id': "u1" if str(x.id) ==  str(s.id) else "u2" ,"name":p.username,"imageUri":"{}{}".format(url,x.avatar)}

        def userM(id):
            u = Profile.objects.get(id=id)

            return {'id': "u1" if str(id) ==  str(s.id) else "u2","name":u.user.username}


        list = {}
        m = []
        
        msg1 = Message.objects.filter(m_sender=s.id).filter(m_reciver=r.id).values()
        msg2 = Message.objects.filter(m_sender=r.id).filter(m_reciver=s.id).values()

        for x in msg1:
                m.append({'id':x['id'],'createdAt':x['created_at'],'content':x['msg'],
                'user':userM(x['m_sender_id'])})
        for x in msg2:
                m.append({'id':x['id'],'createdAt':x['created_at'],'content':x['msg'],
                'user':userM(x['m_sender_id'])})
            
        def myFunc(e):
            return e['createdAt']
        m.sort(key=myFunc)

        # # #{
        # # #   id:1,
        # # #   user:[],
        # # #   messaage:[]
        # # #}

        list = {
            'id':1,
            'users':[user(s),user(r)],
            'message':m
        }

        return Response(list)

