from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from .message import Message
# from .forum import Forum

import secrets
from django.conf import settings

SETTINGS_USERS = settings.SETTINGS_USERS
Permissions = SETTINGS_USERS['Permissions']
PermissionsCode = SETTINGS_USERS['PermissionsCode']

number_message_page = SETTINGS_USERS['NUMBER_PAGE']['number_message_page']

regular_code = PermissionsCode['regular_code']
manager_code = PermissionsCode['manager_code']

class Post(Message):
    id_post = models.CharField(max_length=256, default='')
    title = models.TextField()
    forum_id = models.CharField(max_length=256, default='')
    views = models.IntegerField(default=0)
    messages = models.ManyToManyField(Message, related_name = 'messages', symmetrical=False)
    # forum = models.ForeignKey(Forum, on_delete=models.CASCADE, related_name='forum')

    @classmethod
    def create(self, user, data, permission, title, forum_id):
        id_post = secrets.token_hex(SETTINGS_USERS['LENGTH_ID']['POST'])
        print('id_post', id_post)
        post = self(user=user, id_post=id_post, data=data, permission=permission, last_change_user=user, title=title, forum_id=forum_id)
        return post

    def getPost(self, user=None, page=1):
        print('a1')
        permission = 0
        if user != None:
            permission = user.profile.permission

        listAllMessage = self.messages.all()[(page - 1)*number_message_page: (page)*number_message_page]
        listMessage = []
        for message in listAllMessage:
            if message.permission <= permission:
                listMessage.append(message.getMessage())

        # if listMessage == []:
        #     return -1
        return {
            'title': self.title,
            'user': self.user.username,
            'views': self.views,
            'permission': self.permission,
            'create_date': self.create_date,
            'post_id': self.id_post,
            'data': self.data,
            'messages': listMessage,
        }


    def getHeadPost(self):
        return {
            'user': self.user.username,
            'title': self.title,
            'views': self.views,
            'create_date': self.create_date,
            'post_id': self.id_post,
        }