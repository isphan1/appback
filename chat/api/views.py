from django.core.serializers import serialize
from django.db.models import Q
from rest_framework import viewsets
import rest_framework
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ProfileSerializers, MessageSerializers
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin
from chat.models import Message, Profile
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly
import json

class CreateNewMessage(viewsets.ViewSet):
    
    def list(self,request):

        s = Profile.objects.get(user__username=self.request.data['s_name'])
        r = Profile.objects.get(user__username=self.request.data['r_name'])

        newMsg = Message.objects.create(m_sender=s,m_reciver=r,msg=self.request.data['msg'])

        print(newMsg)

        if newMsg:
            return Response({"msg":"new message create"})

        return Response({"msg":"Something went wrong !"})    
# {
# "s_name":"Alpha",
# "r_name":"Alen",
# }

class UserProfile(viewsets.ViewSet):

    permission_classes = [IsAuthenticatedOrReadOnly]    
    
    def list(self,request):

        id = self.request.data['id']
        
        u = Profile.objects.get(id=id)

        def user(x):
            
            print(x.profile.user.username)

            return [
                    {"id":'u{}'.format(id) ,"name":u.user.username,"imageUri":"http://wbclone.herokuapp.com/media/{}".format(u.avatar)},
                    {"id":'u{}'.format(x.profile.id) ,"name":x.profile.user.username,"imageUri":"http://wbclone.herokuapp.com/media/{}".format(x.profile.avatar)},
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

        def user(x):
            
            p = User.objects.get(id=x.id)

            return {'id': "u1" if str(x.id) ==  str(s.id) else "u2" ,"name":p.username,"imageUri":"http://wbclone.herokuapp.com/media/{}".format(x.avatar)}

        def userM(id):
            u = Profile.objects.filter(id=id).values()
            p = None
            a = ''
            for x in u:
                p = User.objects.filter(id=x['user_id']).values()
                id = x['id']
            for d in p:
                return {'id': "u1" if str(id) ==  str(id_s) else "u2","name":d['username']}

        s = Profile.objects.get(user__username=id_s)
        r = Profile.objects.get(user__username=id_r)

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

