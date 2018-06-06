from channels.generic.websocket import WebsocketConsumer
import json
import datetime
from asgiref.sync import async_to_sync
from chat.models import Message, User
from django.core import serializers


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = 'stream'
        self.room_group_name = 'chat_stream'
        self.user = self.scope['user']

        # Join room group
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

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        sender = text_data_json['sender']

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender
            }
        )

        print("received message from {}".format(sender))

        try:
            Message.objects.create(user=User.objects.get(alias=sender), message=message)
        except Exception as e:
            print(str(e))

    def chat_message(self, event):
        message = event['message']
        sender = event['sender']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'sender': sender
        }))