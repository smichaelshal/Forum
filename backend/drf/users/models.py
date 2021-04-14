from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

import secrets
# from .views import sendMail
from forum.models.private_message import Mailbox
from forum.models.system_message import SystemMessage
from forum.models.message import Message
from forum.models.post import Post

from django.conf import settings
SETTINGS_USERS = settings.SETTINGS_USERS

Permissions = SETTINGS_USERS['Permissions']


class TokenRegister(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=256, default='')
    create_date = models.DateTimeField(default=timezone.now, blank=True)

    def __str__(self):
        return f'{self.user.username} {self.token}'

    def __repr__(self):
        return f'{self.user.username} {self.token}'

    @classmethod
    def create(self, user):
        token = secrets.token_hex(SETTINGS_USERS['TOKEN_REGISTER_LENGTH'])
        tokenRegister = self(user=user, token=token)
        return tokenRegister


class TokenChangePassword(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=256, default='')
    create_date = models.DateTimeField(default=timezone.now, blank=True)

    def __str__(self):
        return f'{self.user.username} {self.token}'

    def __repr__(self):
        return f'{self.user.username} {self.token}'

    @classmethod
    def create(self, user):
        token = secrets.token_hex(SETTINGS_USERS['TOKEN_CHANGE_PASSWORD_LENGTH'])
        tokenChangePassword = self(user=user, token=token)
        return tokenChangePassword

class Profile(models.Model):
    regular_code = 100
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    is_login = models.BooleanField(default=False)

    is_approved = models.BooleanField(default=False)
    permission = models.IntegerField(choices=Permissions, default=regular_code)
    count_login_now = models.PositiveIntegerField(default=0)
    last_login_date = models.DateTimeField(default=timezone.now, blank=True)
    registration_date = models.DateTimeField(default=timezone.now, blank=True)

    mailboxes = models.ManyToManyField(Mailbox, related_name = 'mailboxes', symmetrical=False)
    system_messages = models.ManyToManyField(SystemMessage, related_name = 'system_messages', symmetrical=False)
    messages = models.ManyToManyField(Message, related_name = 'my_messages', symmetrical=False)
    posts = models.ManyToManyField(Post, related_name = 'my_posts', symmetrical=False)

    
    @classmethod
    def create(self, user):
        tokenRegister = TokenRegister.create(user=user)
        tokenRegister.save()

        profile = self(user=user)
        return profile

    def __str__(self):
        return f'{self.user.username}'

    def __repr__(self):
        return f'{self.user.username}'

    def getAllHeadMailbox(self):
        listHeadMessages = []
        mailboxes = self.mailboxes.all()
        for mailbox in mailboxes:
            listHeadMessages.append(mailbox.getHeadMailbox())
        return listHeadMessages

    def getAllMessages(self, permission):
        messages = self.messages.all()
        listMessages = []
        for message in messages:
            if message.permission <= permission:
                listMessages.append(message.getMessage())
        return listMessages

    def getAllPosts(self, permission):
        posts = self.posts.all()
        listPosts = []
        for post in posts:
            if post.permission <= permission:
                listPosts.append(post.getHeadPost())
        return listPosts

    def getProfilePermission(self):
        return  {
           'permission', self.permission
        }

    def getAllSystemMessage(self, permission):
        system_messages = self.system_messages.all()
        listSystemMessages = []
        for message in system_messages:
            if SystemMessage.permission <= permission:
                listSystemMessages.append(message.getSystemMessage())
        return listSystemMessages
