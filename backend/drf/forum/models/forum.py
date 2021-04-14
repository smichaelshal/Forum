from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from .post import Post

# from .category import Category

import secrets
from django.conf import settings

SETTINGS_USERS = settings.SETTINGS_USERS
Permissions = SETTINGS_USERS['Permissions']
PermissionsCode = SETTINGS_USERS['PermissionsCode']
number_post_page = SETTINGS_USERS['NUMBER_PAGE']['number_post_page']

regular_code = PermissionsCode['regular_code']
manager_code = PermissionsCode['manager_code']

class Forum(models.Model):
    regular_code = 0

    posts = models.ManyToManyField(Post, related_name = 'posts', symmetrical=False)
    mangers = models.ManyToManyField(User, related_name = 'mangers', symmetrical=False)
    inspector = models.ManyToManyField(User, related_name = 'inspectors', symmetrical=False)
    id_forum = models.CharField(max_length=256, default='')
    # category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category')
    category_id = models.CharField(max_length=256, default='')
    permission = models.IntegerField(choices=Permissions, default=regular_code)
    name = models.TextField()


    @classmethod
    def create(self, name, permission, category_id):
        id_forum = secrets.token_hex(SETTINGS_USERS['LENGTH_ID']['FORUM'])
        forum = self(name=name, id_forum=id_forum, category_id=category_id, permission=permission)
        return forum


    def getForum(self, user=None, page=1):
        permission = 0
        if user != None:
            permission = user.profile.permission

        listAllPosts = self.posts.all()[(page - 1)*number_post_page: (page)*number_post_page]
        listPosts = []
        for post in listAllPosts:
            print(post.permission <= permission, post.permission, permission)
            if post.permission <= permission:
                listPosts.append(post.getHeadPost())
        if listPosts == []:
            return -1
        return {
            'title': self.name,
            'permission': self.permission,
            'id_forum': self.id_forum,
            'category_id': self.category_id,
            'posts': listPosts,
        }

    def getHeadForum(self):
        return {
            'name': self.name,
            'id_forum': self.id_forum,
            'permission': self.permission,
        }