from django.db import models
from django.db.models import fields
from rest_framework import serializers
from chat.models import Profile,Message
from django.contrib.auth.models import User

class ProfileSerializers(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"
        depth=1

class MessageSerializers(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = "__all__"

    def create(self,validate_data):

        print(validate_data)

class UserSerializer(serializers.ModelSerializer):
    
    username = serializers.CharField(style={'input_type':'text'},write_only=True)
    # email = serializers.CharField(style={'input_type':'text'},write_only=True)
    password = serializers.CharField(style={'input_type':'password'},write_only=True)
    # token_response = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['username','password']
        extra_kwargs = {'passwrod':{'write_only':True}}

    # def get_token_response(self,obj):
    #     user = obj
    #     payload = jwt_payload_handler(user)
    #     token = jwt_encode_handler(payload)
    #     response = jwt_response_payload_handler(token,user,request=None)

    #     return response

    def validate_username(self,value):
        qs = User.objects.filter(username__iexact=value)
        print(value)
        if qs.exists():
            raise serializers.ValidationError('This username is already taken')
        return value

    # def validate_email(sefl,value):
    #     qs = User.objects.filter(email__iexact=value)
    #     if qs.exists():
    #         raise serializers.ValidationError('This email is already taken')
    #     return value

    def create(self,validate_data):
        username = validate_data.get('username')

        # email = validate_data.get('email')
        password = validate_data.get('password')
        user = User(username=username)
        # user = User(username=username,email=email)
        user.set_password(password)
        user.save()

        return user