from django.db import models
from django.db.models import fields
from rest_framework.serializers import ModelSerializer
from chat.models import Profile,Messages

class ProfileSerializers(ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"
        depth=1

class MessageSerializers(ModelSerializer):

    class Meta:
        model = Messages
        fields = "__all__"
        depth=1