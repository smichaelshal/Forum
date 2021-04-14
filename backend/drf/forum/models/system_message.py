from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from .message import HistoryMessage

import secrets
from django.conf import settings

SETTINGS_USERS = settings.SETTINGS_USERS
Permissions = SETTINGS_USERS['Permissions']
PermissionsCode = SETTINGS_USERS['PermissionsCode']

regular_code = PermissionsCode['regular_code']
manager_code = PermissionsCode['manager_code']
inspector_code = PermissionsCode['inspector_code']

class SystemMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_created')
    create_date = models.DateTimeField(default=timezone.now, blank=True)
    permission = models.IntegerField(choices=Permissions, default=inspector_code)
    last_change_date = models.DateTimeField(default=timezone.now, blank=True)
    last_change_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='last_change_user_message')
    history = models.ManyToManyField(HistoryMessage, related_name = 'history_system_message', symmetrical=False)
    data = models.TextField()

    @classmethod
    def create(self, user, data, permission):
        system_message_id = secrets.token_hex(SETTINGS_USERS['LENGTH_ID']['SystemMessage'])
        system_message = self(user=user, data=data, permission=permission, last_change_user=user, system_message_id=system_message_id)
        return system_message

    def getSystemMessage(self):
        return {
            'date': self.create_date,
            'permission': self.permission,
            'data': self.data,
            'user': self.user,
            'permission': self.permission,
        }