from channels.generic.websocket import WebsocketConsumer
import json
import datetime
from asgiref.sync import async_to_sync
from chat.models import Message, User
from django.db.models import Count


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
        print(text_data)

        text_data_json = json.loads(text_data)
        type = text_data_json['type']

        if type == "chat_message":
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

        if type == "stats":
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'leader': 'test leader',
                    'messages_count': 2,
                    'type': 'stats'
                }
            )

    def chat_message(self, event):
        message = event['message']
        sender = event['sender']

        # print(event)

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'type': 'chat_message',
            'message': message,
            'sender': sender
        }))

    def stats(self, event):
        print("stats method called")
        timedelta = datetime.datetime.now() - datetime.timedelta(minutes=1)
        messages = Message.objects.filter(created__gte=timedelta)
        messages_count = messages.count()
        leaders = messages.values("user").annotate(uc=Count("user")).order_by('-uc')

        if len(leaders):
            leader = User.objects.get(id=leaders[0]['user']).alias
        else:
            leader = "-"

        self.send(text_data=json.dumps({
            'leader': leader,
            'messages_count': messages_count,
            'type': 'stats'
        }))
