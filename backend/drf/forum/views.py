from django.contrib.auth.models import User
from django.conf import settings

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_200_OK,
    HTTP_404_NOT_FOUND,
)

SETTINGS_USERS = settings.SETTINGS_USERS
PermissionsCode = SETTINGS_USERS['PermissionsCode']
regular_code = PermissionsCode['regular_code']


from users.utilities import checkParamsJson, get_user_from_request, checkPermissions, sendMail

from .models.post import Post
from .models.forum import Forum
from .models.category import Category
from .models.message import Message


class GetPost(APIView):
    permission_classes = (AllowAny,)
    
    @checkParamsJson(listParams=['id', 'page'])
    @checkPermissions(permission=0)
    def post(self, request):
        idPost = request.data['id']
        page = request.data['page']
        permission = 0
        user = None
        try:
            user = get_user_from_request(self, request)
            permission = user.profile.permission
        except:
            pass

        try:
            post = Post.objects.get(id_post=idPost)
            print('post', post)
            if post.permission > permission:
                raise Exception('Permission is required')
        except:
            return Response({"msg": 'the post is not exsit'}, status=HTTP_400_BAD_REQUEST)

        print('b1')
        jsonResponse = post.getPost(user)
        print('b2')
        # return Response({"msg": 'the post is not exsit'}, status=HTTP_400_BAD_REQUEST)
        if jsonResponse == -1:
            return Response({"msg": 'the page not found'}, status=HTTP_404_NOT_FOUND)



        return Response({"post": jsonResponse}, status=HTTP_200_OK)


class GetForum(APIView):
    permission_classes = (AllowAny,)
    
    @checkParamsJson(listParams=['id', 'page'])
    @checkPermissions(permission=0)
    def post(self, request):
        idForum = request.data['id']
        page = request.data['page']
        permission = 0
        user = None

        try:
            user = get_user_from_request(self, request)
            permission = user.profile.permission
        except:
            pass

        try:
            forum = Forum.objects.get(id_forum=idForum)
            if forum.permission > permission:
                raise Exception('Permission is required')
        except:
            return Response({"msg": 'the forum is not exsit'}, status=HTTP_400_BAD_REQUEST)

        jsonResponse = forum.getForum(user, page)
        if jsonResponse == -1:
            return Response({"msg": 'the page not found'}, status=HTTP_404_NOT_FOUND)

        return Response({"forum": jsonResponse}, status=HTTP_200_OK)


class GetCategory(APIView):
    permission_classes = (AllowAny,)
    
    @checkParamsJson(listParams=['id'])
    @checkPermissions(permission=0)
    def post(self, request):
        idCategory= request.data['id']
        permission = 0
        user = None

        try:
            user = get_user_from_request(self, request)
            permission = user.profile.permission
        except:
            pass

        try:
            category = Category.objects.get(id_category=idCategory)
            if category.permission > permission:
                raise Exception('Permission is required')
        except:
            # return Response({"msg": 'the category is not exsit'}, status=HTTP_400_BAD_REQUEST)
            return Response({"msg": 'the category is not exsit'}, status=HTTP_404_NOT_FOUND)

        jsonResponse = category.getCategory(user)
        if jsonResponse == -1:
            return Response({"msg": 'the page not found'}, status=HTTP_404_NOT_FOUND)

        return Response({"category": jsonResponse}, status=HTTP_200_OK)

class CreateCategory(APIView):
    permission_classes = (IsAuthenticated,)
    
    @checkParamsJson(listParams=['name', 'permission'])
    @checkPermissions(permission=PermissionsCode['ceo_code'])
    # @checkPermissions(permission=regular_code)
    def post(self, request):
        name = request.data['name']
        permissionCategory = request.data['permission']
        try:
            categoryTemp = Category.objects.get(name=name)
            return Response({"msg": 'The category name is busy'}, status=HTTP_400_BAD_REQUEST)
        except:
            pass
        category = Category.create(name=name, permission=permissionCategory)
        category.save()
        return Response({"msg": 'The category created'}, status=HTTP_200_OK)

class CreateForum(APIView):
    permission_classes = (IsAuthenticated,)
    
    @checkParamsJson(listParams=['name', 'permission', 'category_id'])
    @checkPermissions(permission=PermissionsCode['ceo_code'])
    # @checkPermissions(permission=regular_code)
    def post(self, request):
        name = request.data['name']
        permissionForum = request.data['permission']
        category_ids = request.data['category_id']

        try:
            category = Category.objects.get(id_category=category_ids)
        except:
            return Response({"msg": 'The category does not exist'}, status=HTTP_400_BAD_REQUEST)

        try:
            forumTemp = category.forums.get(name=name)
            return Response({"msg": 'The forum name is busy'}, status=HTTP_400_BAD_REQUEST)
        except:
            forum = Forum.create(name=name, permission=permissionForum, category_id=category_ids)
            forum.save()
            category.forums.add(forum)
            category.save()

        return Response({"msg": 'The forum created'}, status=HTTP_200_OK)

class CreatePost(APIView):
    permission_classes = (IsAuthenticated,)
    
    @checkParamsJson(listParams=['title', 'data', 'forum_id'])
    @checkPermissions(permission=regular_code)
    def post(self, request):
        data = request.data['data']
        title = request.data['title']
        forum_ids = request.data['forum_id']
        user = get_user_from_request(self, request)
        try:
            permission = request.data['permission']
            if permission <= user.profile.permission:
                permission = regular_code
        except:
            permission = regular_code

        try:
            forum = Forum.objects.get(id_forum=forum_ids)
        except:
            return Response({"msg": 'The forum does not exist'}, status=HTTP_400_BAD_REQUEST)

        post = Post.create(user=user, data=data, permission=permission, forum_id=forum_ids, title=title)
        post.save()

        forum.posts.add(post)
        forum.save()
        
        return Response({"msg": 'The post created', 'id': post.id_post}, status=HTTP_200_OK)

class CreateMessage(APIView):
    permission_classes = (IsAuthenticated,)
    
    @checkParamsJson(listParams=['data', 'post_id'])
    @checkPermissions(permission=regular_code)
    def post(self, request):
        data = request.data['data']
        post_id = request.data['post_id']
        user = get_user_from_request(self, request)

        if data == None:
            data = "test"
        try:
            permission = request.data['permission']
            if permission <= user.profile.permission:
                permission = regular_code
        except:
            permission = regular_code

        try:
            post = Post.objects.get(id_post=post_id)
        except:
            return Response({"msg": 'The post does not exist'}, status=HTTP_400_BAD_REQUEST)

        message = Message.create(user=user, data=data, permission=permission, is_quoted=False, post_id=post_id)
        message.save()

        post.messages.add(message)
        post.save()

        return Response({"msg": 'The message created', 'id': message.id_message}, status=HTTP_200_OK)


class GetListCategories(APIView):
    permission_classes = (AllowAny,)
    
    @checkParamsJson(listParams=[])
    @checkPermissions(permission=0)
    def post(self, request):
        permission = 100
        try:
            user = get_user_from_request(self, request)
            permission = user.profile.permission
        except:
            pass
        categories = Category.objects.all()
        listJsonCategory = []
    
        for category in categories:
            if category.permission <= permission:
                listJsonCategory.append(category.getHeadCategory())

        return Response({"listCategory": listJsonCategory}, status=HTTP_200_OK)
        
        
