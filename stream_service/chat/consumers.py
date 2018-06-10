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

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'user_connected',
                'user': self.scope['user'].alias,
                'user_id': self.scope['user'].id,
                "created": datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%SZ')
            }
        )

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):

        text_data_json = json.loads(text_data)
        type = text_data_json['type']

        if type == "stats":
            self.stats()

        if type == "chat_message":
            message = text_data_json['message']
            sender = text_data_json['sender']
            sender_id = text_data_json['sender_id']

            # Send message to room group
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'sender': sender,
                    'sender_id': sender_id
                }
            )

            try:
                Message.objects.create(user=User.objects.get(id=sender_id), message=message)
            except Exception as e:
                print(str(e))

    def user_connected(self, event):
        self.send(text_data=json.dumps({
            'type': 'user_connected',
            'user': event['user'],
            'user_id': event['user_id'],
            "created": event['created']
        }))

    def chat_message(self, event):
        message = event['message']
        sender = event['sender']
        sender_id = event['sender_id']

        self.send(text_data=json.dumps({
            'type': 'chat_message',
            'message': message,
            'sender': sender,
            'sender_id': sender_id,
            "created": datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%SZ')
        }))

    def stats(self):
        timedelta = datetime.datetime.now() - datetime.timedelta(minutes=1)
        messages = Message.objects.filter(created__gte=timedelta)
        messages_count = messages.count()
        leaders = messages.values("user").annotate(uc=Count("user")).order_by('-uc')

        if len(leaders):
            leader = User.objects.get(id=leaders[0]['user']).alias
        else:
            leader = " "

        self.send(text_data=json.dumps({
            'leader': leader,
            'messages_count': messages_count,
            'type': 'stats'
        }))
