from rest_framework import serializers
from .models import Message

class MessageSerilazer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields =('username','content','timestamp')