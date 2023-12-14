from channels.generic.websocket import AsyncWebsocketConsumer
import json
from channels.db import database_sync_to_async
from .models import Message
from django.contrib.auth.models import User




class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        # this is a nested dictionary and it will return the room_id which we are passing through the url
        current_user_id = self.scope['url_route']['kwargs']['id']
        # other_user_id = int(self.scope['query_string'])
        # print(other_user_id)

        self.room_id = current_user_id
        self.room_group_name = f'group_{self.room_id}'

        # the channel_layer.group_add() takes two arguments
        # the name of the group to add the connection to --> self.room_group_name
        # and the name of the websocket connection ---> self.channel_name
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        await super().disconnect(close_code)

        async def receive(self, text_data=None):
            try:
                data = json.loads(text_data)
                message = data.get("message")
                sender_id = data.get("sender_id")
                sender_username = data.get("sender_username")

                if message is not None and sender_id is not None and sender_username is not None:
                    await self.save_message(
                        sender=sender_id, message=message, thread_name=self.room_group_name, sender_username=sender_username
                    )

                    print("This is the channel group name: ", self.room_group_name)

                    # Send the message to the channel layer
                    await self.channel_layer.group_send(
                        self.room_group_name,
                        {
                            "type": "chat_message",
                            "message": message,
                            "senderId": sender_id,
                            "senderUsername": sender_username,
                        },
                    )
                else:
                    print("Received JSON data is missing required fields.")

            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")
            except KeyError as e:
                print(f"Error accessing key: {e}")

    async def chat_message(self, event):
        print("Its entering here alright!!!")

        message = event["message"]
        sender_id = event["senderId"]
        sender_username = event["senderUsername"]

        await self.send(
            text_data=json.dumps(

                {
                    "message": message,
                    "senderId": sender_id,
                    "senderUsername": sender_username,
                }
            ),

        )

    @database_sync_to_async
    def save_message(self, sender, sender_username, message, thread_name):
        user_instance = User.objects.get(id=sender)

        Message.objects.create(
            sender=user_instance, message=message, sender_username=user_instance.username, thread_name=thread_name)