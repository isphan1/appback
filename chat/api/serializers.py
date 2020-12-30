from django.db import models
from django.db.models import fields
from rest_framework.serializers import ModelSerializer
from chat.models import Profile,Message

class ProfileSerializers(ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"
        depth=1

class MessageSerializers(ModelSerializer):

    class Meta:
        model = Message
        fields = "__all__"

    def create(self,validate_data):

        print(validate_data)

        