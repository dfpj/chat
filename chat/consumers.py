import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .serializers import MessageSerilazer
from .models import Message, Chat
from rest_framework.renderers import JSONRenderer
from django.contrib.auth.models import User, AnonymousUser


class ChatConsumer(WebsocketConsumer):

    def new_message(self, message):
        obj = Message.objects.create(
            author=User.objects.get(username=self.user),
            content=message,
            chat=Chat.objects.get(name=self.room_name)
        )
        message = self.message_serializer(obj)
        self.send_to_chat_message(eval(message))

    def fetch_message(self, data):
        queryset = Message.objects.filter(chat__name=self.room_name)
        messages = self.message_serializer(queryset)
        self.chat_message({'message': eval(messages), 'command': 'fetch_message'})

    def message_serializer(self, queryset):
        isManyObject = lambda qs: True if qs.__class__.__name__ == 'QuerySet' else False
        serialized = MessageSerilazer(queryset, many=isManyObject(queryset))
        contnet = JSONRenderer().render(serialized.data)
        return contnet

    def image(self,data):
        #send_to_chat_message => data in message key and set command key to img
        pass

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        self.user = self.scope.get('user')
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data=None, bytes_data=None):
        text_data_dict = json.loads(text_data)
        message = text_data_dict['message']
        command = text_data_dict['command']

        if command == 'new_message':
            self.new_message(message)
        elif command == 'fetch_message':
            self.fetch_message(None)
        elif command == 'img':
            self.image(message)

    def send_to_chat_message(self, message):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'command': 'new_message'
            }
        )

    def chat_message(self, event):
        self.send(text_data=json.dumps(event))
