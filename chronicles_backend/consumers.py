import json
from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
from channels.generic.websocket import WebsocketConsumer
from channels.auth import get_user
from .models import BugReport, Comment


class CommentConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bug_id = self.scope['url_route']['kwargs']['pk']

    def connect(self):
        self.user = async_to_sync(get_user)(self.scope)
        if self.user.is_authenticated:
            try:
                bug_report = BugReport.objects.get(pk=self.bug_id)
                async_to_sync(self.channel_layer.group_add)(
                    self.bug_id,
                    self.channel_name
                )
                self.accept()
            except BugReport.DoesNotExist:
                self.close()
        else:
            self.close()

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.bug_id,
            self.channel_name
        )

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        async_to_sync(self.channel_layer.group_send)(
            self.bug_id,
            {
                'type': 'send_comment',
                'message': message
            }
        )

    def send_comment(self, event):
        message = event['message']
        self.send(text_data=json.dumps({
            'message': message
        }))
