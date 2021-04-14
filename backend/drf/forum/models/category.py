from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from .forum import Forum


import secrets
from django.conf import settings

SETTINGS_USERS = settings.SETTINGS_USERS
Permissions = SETTINGS_USERS['Permissions']

class Category(models.Model):
    regular_code = 0

    forums = models.ManyToManyField(Forum, related_name = 'forums_category', symmetrical=False)
    inspector = models.ManyToManyField(User, related_name = 'inspectors_category', symmetrical=False)
    id_category = models.CharField(max_length=256, default='')
    permission = models.IntegerField(choices=Permissions, default=regular_code)
    name = models.TextField()

    @classmethod
    def create(self, name, permission):
        id_category = secrets.token_hex(SETTINGS_USERS['LENGTH_ID']['CATEGORY'])
        category = self(name=name, id_category=id_category, permission=permission,)
        return category

    def getCategory(self, user=None):
        permission = 0
        if user != None:
            permission = user.profile.permission

        listAllForums = self.forums.all()
        listForums = []
        for forum in listAllForums:
            if forum.permission <= permission:
                listForums.append(forum.getHeadForum())
        if listForums == []:
            return -1
        return {
            'forums': listForums,
            'id_category': self.id_category,
            'permission': self.permission,
        }
    def getHeadCategory(self):
        return {
            'name': self.name,
            'id': self.id_category,
            'permission': self.permission,
        }