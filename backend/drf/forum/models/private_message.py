from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from .message import Message

import secrets
from django.conf import settings

SETTINGS_USERS = settings.SETTINGS_USERS
Permissions = SETTINGS_USERS['Permissions']
PermissionsCode = SETTINGS_USERS['PermissionsCode']

regular_code = PermissionsCode['regular_code']
manager_code = PermissionsCode['manager_code']
inspector_code = PermissionsCode['inspector_code']

class PrivateMessage(models.Model):
    user_send = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_send')
    addressee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addressee')
    create_date = models.DateTimeField(default=timezone.now, blank=True)
    data = models.TextField()
    private_message_id = models.CharField(max_length=256, default='')
    permission = models.IntegerField(choices=Permissions, default=regular_code)

    @classmethod
    def create(self, user, data, permission, addressee):
        private_message_id = secrets.token_hex(SETTINGS_USERS['LENGTH_ID']['PrivateMessage'])
        private_message = self(user=user, data=data, permission=permission, addressee=addressee, private_message_id=private_message_id)
        return private_message
    
    def getMessage(self):
        return {
                'user': self.user_send,
                'date': self.create_date,
                'data': self.data,
                'id': self.private_message_id,
                'permission': self.permission,
            }


class Mailbox(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_send_private_message')
    other_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='other_user')
    private_message = models.ManyToManyField(PrivateMessage, related_name = 'private_message', symmetrical=False)
    mailbox_id = models.CharField(max_length=256, default='')

    last_date = models.DateTimeField(default=timezone.now, blank=True)
    last_message = models.ForeignKey(PrivateMessage, on_delete=models.CASCADE, related_name='last_private_message')
    @classmethod
    def create(self, user, other_user):
        mailbox_id = secrets.token_hex(SETTINGS_USERS['LENGTH_ID']['Mailbox'])
        mailbox = self(user=user, other_user=other_user, mailbox_id=mailbox_id)
        return mailbox
    
    def getMailbox(self):
        listMessages = []
        private_messages = self.private_message.all()
        for message in private_messages:
            listMessages.append(message.getMessage())
        return listMessages

    def getHeadMailbox(self):
        return {
                'other_user': self.other_user,
                'last_message': self.last_message,
                'last_date': self.last_date,
                'id': self.mailbox_id
            }

    def sendMessage(self, message):
        self.private_message.add(message)
        self.private_message.save()

        newMessage = PrivateMessage.create(user=message.other_user, data=message.data, permission=message.permission, addressee=mailbox.user)
        newMessage.save()

        mailboxes = message.other_user.profile.mailboxes
        mailbox = mailboxes.get(mailbox_id=idMailbox)
        mailbox.add(newMessage)
        mailbox.save()

