from channels.generic.websocket import AsyncWebsocketConsumer
import json
from channels.db import database_sync_to_async





class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        # this is a nested dictionary and it will return the room_id which we are passing through the url
        # current_user_id = self.scope['url_route']['kwargs']['id']
        # other_user_id = int(self.scope['query_string'])
        # print(other_user_id)

        self.room_id = 'test'
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
        data = json.loads(text_data)
        message = data["message"]
        sender_id = data["sender_id"]
        sender_username = data["sender_username"]

       

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
