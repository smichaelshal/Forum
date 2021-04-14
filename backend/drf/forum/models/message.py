from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

import secrets
from django.conf import settings

SETTINGS_USERS = settings.SETTINGS_USERS
Permissions = SETTINGS_USERS['Permissions']

class HistoryMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now, blank=True)
    data = models.TextField()

class Message(models.Model):
    regular_code = 0
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    data = models.TextField()
    permission = models.IntegerField(choices=Permissions, default=regular_code)
    create_date = models.DateTimeField(default=timezone.now, blank=True)

    is_quoted = models.BooleanField(default=False)
    quoteds = models.ManyToManyField('self', related_name = 'quoted_messages', symmetrical=False)

    last_change_date = models.DateTimeField(default=timezone.now, blank=True)
    last_change_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='last_change_user')
    history = models.ManyToManyField(HistoryMessage, related_name = 'history_message', symmetrical=False)
    
    id_message = models.CharField(max_length=256, default='')
    post_id = models.CharField(max_length=256, default='')

    @classmethod
    def create(self, user, data, permission, is_quoted, post_id):
        id_message = secrets.token_hex(SETTINGS_USERS['LENGTH_ID']['MESSAGE'])
        message = self(user=user, id_message=id_message, data=data, permission=permission, last_change_user=user, post_id=post_id)
        return message

    def change(self, data, user):
        history_message = HistoryMessage(user=self.last_change_user, date=self.last_change_date, data=self.data)
        history_message.save()
        self.history.add(history_message)
        self.data = data
        self.last_change_date = timezone.now()
        self.last_change_user = user
        self.save()

    def changePermission(self, permission):
        self.permission = permission
        self.save()

    def getMessage(self):
        return {
            "user": self.user.username,
            "data": self.data,
            "permission": self.permission,
            "create_date": self.create_date,
            "id_message": self.id_message,
            "post_id": self.post_id,
        }

