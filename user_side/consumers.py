import json
from django.shortcuts import get_object_or_404
from channels.generic.websocket import WebsocketConsumer,AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
from django.db.models import Q
from channels.layers import get_channel_layer
from channels.auth import get_user
from channels.db import database_sync_to_async
from .models import Room, Message,User
# from user_side.models import Follow, Notification, News
import json
from django.dispatch import receiver
from django.db.models.signals import pre_save,post_save,post_delete



class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        print(self.room_name,'aksnkajshdkajhda______________ASSA_____________________+')
        k=self.room_name
        try:
            target_user = get_object_or_404(User, id=k)
            print(target_user,'kiteee')
        except:
            target_user = ""

        if target_user is not None:
            print('asadas________akooo')
            target_user = User.objects.get(id=k)
            users = [target_user]
            room_qs = Room.objects.filter(users=k).filter(users=k)

            if not room_qs.exists():
                self.room = Room.objects.create()
                self.room.users.set(users)
            else:
                self.room = room_qs.first()

            self.room_group_name = self.room.token
            print('connected')

            async_to_sync(self.channel_layer.group_add)(
                self.room_group_name, self.channel_name
            )

            self.accept()
    
    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        sender_id = int(text_data_json['sender_id'])  # Convert sender_id to an integer

        # Retrieve the sender User instance from the database
        sender_user = get_object_or_404(User, id=sender_id)
        
        msg = Message.objects.create(
            room=self.room,
            sender=sender_user,  # Use the User instance as sender
            message=str(message)
        )

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, 
            {
                "type": "chat_message",
                "message": msg.message,
                "sender": msg.sender.id
            }
        )
        print('succsess')
        
    def chat_message(self, event):
        print(event,'____________p___________')
        message = event["message"]
        sender = event["sender"]
        self.send(text_data=json.dumps({
            "message": event["message"],
            "sender": event["sender"]
        }))
        
        

#notificatioj

# import jwt
# from django.conf import settings


# from urllib.parse import parse_qs

# class NotificationConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         query_string = self.scope['query_string'].decode('utf-8')
#         query_params = parse_qs(query_string)
#         user_id = query_params.get('user_id')[0] if 'user_id' in query_params else None

#         if user_id:
#             await self.accept()
#             await self.channel_layer.group_add(
#                 f'user_{user_id}',
#                 self.channel_name
#             )

#     async def disconnect(self, close_code):
#         query_string = self.scope['query_string'].decode('utf-8')
#         query_params = parse_qs(query_string)
#         user_id = query_params.get('user_id')[0] if 'user_id' in query_params else None

#         if user_id:
#             await self.channel_layer.group_discard(
#                 f'user_{user_id}',
#                 self.channel_name
#             )
       
#     async def send_notification(self, event):
#         message = event['message']
#         await self.send(text_data=json.dumps({
#             'message': message
#         }))


