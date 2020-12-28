from django.core.checks import messages
from django.core.serializers import serialize
from django.db.models import Q
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ProfileSerializers, MessageSerializers
from rest_framework.generics import ListAPIView
from rest_framework.mixins import RetrieveModelMixin
from chat.models import Messages, Profile
from django.contrib.auth.models import User
import json

class UserProfile(viewsets.ViewSet):
    
    def list(self,request,id=None):
        
        u = Profile.objects.get(id=id)

        m = u.friends.all()

        def user(x):
            p = Profile.objects.filter(id=x.profile.id).values()
            
            for z in p:

                return [
                    {"id":'u{}'.format(id) ,"name":u.user.username,"imageUri":"http://wbclone.herokuapp.com/media/{}".format(u.avatar)},
                    {"id":'u{}'.format(z['id']) ,"name":x.username,"imageUri":"http://wbclone.herokuapp.com/media/"+z['avatar']},
                ]


        friends = [u for u in m]            
        list = []
        icd = 1
        for f in friends:
            m = []
            msg1 = Messages.objects.filter(sender_p=id).filter(reciver_p=f.profile.id).values()
            msg2 = Messages.objects.filter(sender_p=f.profile.id).filter(reciver_p=id).values()

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
    # serializer_class = MessageSerializers

    def list(self,request,id_s=None,id_r=None):

        def user(x):
            for i in x:
                p = User.objects.filter(id=i['user_id']).values()
                a = i['avatar']
                id = i['id']
                for d in p:
                    return {'id': "u1" if str(id) ==  str(id_s) else "u2" ,"name":d['username'],"imageUri":"http://wbclone.herokuapp.com/media/"+a}

        def userM(id):
            u = Profile.objects.filter(id=id).values()
            p = None
            a = ''
            for x in u:
                p = User.objects.filter(id=x['user_id']).values()
                id = x['id']
            for d in p:
                return {'id': "u1" if str(id) ==  str(id_s) else "u2","name":d['username']}

        s = Profile.objects.filter(id=id_s).values()
        r = Profile.objects.filter(id=id_r).values()
        list = {}
        m = []
        msg1 = Messages.objects.filter(sender_p=id_s).filter(reciver_p=id_r).values()
        msg2 = Messages.objects.filter(sender_p=id_r).filter(reciver_p=id_s).values()

        for x in msg1:
                m.append({'id':x['id'],'createdAt':x['created_at'],'content':x['msg'],'user':userM(x['sender_p_id'])})
        for x in msg2:
                m.append({'id':x['id'],'createdAt':x['created_at'],'content':x['msg'],'user':userM(x['sender_p_id'])})

        # print(m[0]['created_at'])
            
        def myFunc(e):
            return e['createdAt']
        m.sort(key=myFunc)

        # #{
        # #   id:1,
        # #   user:[],
        # #   messaage:[]
        # #}

        list = {
            'id':1,
            'users':[user(s),user(r)],
            'message':m
        }

        
        return Response(list)
    