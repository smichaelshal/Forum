from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings

from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_200_OK,
    HTTP_403_FORBIDDEN,
)

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.models import TokenUser

from .serializers import (
    UserSerializer,
    RegisterSerializer,
)

from .models import TokenRegister, TokenChangePassword, Profile

import functools
import secrets

SETTINGS_USERS = settings.SETTINGS_USERS
PermissionsCode = SETTINGS_USERS['PermissionsCode']
regular_code = PermissionsCode['regular_code']
inspector_code = PermissionsCode['inspector_code']


from .utilities import checkParamsJson, get_user_from_request, checkPermissions, sendMail

from forum.models.private_message import Mailbox
from forum.models.system_message import SystemMessage
from forum.models.private_message import PrivateMessage

class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    @checkParamsJson(listParams=['username', 'password', 'email'])
    def post(self, request, *args, **kwargs):
        """
            User registration
            params: request,
            return response HTTP 200 OK
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            email = request.data['email']
        except:
            return Response({"email": ["This field may not be blank."]}, status=HTTP_400_BAD_REQUEST)
        listUsersEmail = User.objects.all().filter(email=email)
        if email == '':
            return Response({"email": ["This field may not be blank."]}, status=HTTP_400_BAD_REQUEST)

        if len(listUsersEmail) != 0:
            return Response({"email": ["A user with that email already exists."]}, status=HTTP_400_BAD_REQUEST)
        user = serializer.save()
        profile = Profile.create(user=user)
        profile.save()
        token = TokenRegister.objects.get(user=user)
        titleToRegister = f'Website verification verification {user.username}'
        data = f'The token is {token}'
        try:
            sendMail(user.email, titleToRegister, data)
        except:
            user.delete()
            return Response({"email": ["This email does not exist"]}, status=HTTP_400_BAD_REQUEST) #<-

        return Response({"msg": "You have successfully registered"}, status=HTTP_200_OK)

class LoginApi(APIView):
    permission_classes = (AllowAny,)
    
    @checkParamsJson(listParams=['username','password'])
    @checkPermissions(permission=0)
    def post(self, request):
        username = request.data['username']
        password = request.data['password']

        user = authenticate(username=username, password=password)
        if not (user is None):
            try:
                tokenRegister = TokenRegister.objects.get(user=user)
                return Response({"msg": "The email needs to be confirmed"}, status=HTTP_400_BAD_REQUEST)
            except:
                if (SETTINGS_USERS['MAX_LOGIN_NOW'] == -1) or SETTINGS_USERS['MAX_LOGIN_NOW'] > user.profile.count_login_now:
                    if user.profile.permission < 0:
                        return Response({"msg": "The user is in ban"}, status=HTTP_400_BAD_REQUEST)
                else:
                    return Response({"msg": "Too connected to the user"}, status=HTTP_400_BAD_REQUEST)

            tokens = self.get_tokens_for_user(user)
            return Response(tokens, status=HTTP_200_OK)
        else:
            return Response({"msg": "The username or password is incorrect"}, status=HTTP_400_BAD_REQUEST)
    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

class ConfirmedEmailApi(APIView):
    permission_classes = (AllowAny,)
    
    @checkParamsJson(listParams=['token'])
    @checkPermissions(permission=0)
    def post(self, request):
        tokenStr = request.data['token']
        
        try:
            token = TokenRegister.objects.get(token=tokenStr)
            user = token.user
            profile = user.profile
            profile.is_approved = True
            profile.save()
            token.delete()
            return Response({"msg": "The user successfully confirmed"},
                status=HTTP_200_OK)
        except:
            return Response({"msg": "The token is incorrect"},
                status=HTTP_400_BAD_REQUEST)


class ResetPasswordApi(APIView):
    permission_classes = (AllowAny,)
    
    @checkParamsJson(listParams=['email'])
    @checkPermissions(permission=0)
    def post(self, request):
        email = request.data['email']
        try:
            user = User.objects.all().filter(email=email)[0]
        except:
            return Response({"msg": "The email is unregistered"},
             status=HTTP_400_BAD_REQUEST)
        if not user.profile.is_approved:
            return Response({"msg": "The email not approved"}, status=HTTP_400_BAD_REQUEST)
        try:
            tokenChangePassword = TokenChangePassword.create(user=user)
            tokenChangePassword.save()
        except:
            tokenChangePassword = user.tokenchangepassword
        token_str = tokenChangePassword.token
        titleToRegister = f'Password Reset {user.username}'
        data = f'The token to reset password is {token_str}'
        sendMail(user.email, titleToRegister, data)
        return Response({"msg": "A password reset token has been sent to you"}, status=HTTP_200_OK)
    
    @checkParamsJson(listParams=['token', 'password'])
    @checkPermissions(permission=0)
    def put(self, request):
        token = request.data['token']
        password = request.data['password']

        try:
            tokenChangePassword = TokenChangePassword.objects.get(token=token)
            user = tokenChangePassword.user
            maxDateToResetePassword = tokenChangePassword.create_date + SETTINGS_USERS['LENGTH_DATE_TOKEN_RESET_PASSWORD']
            if timezone.now() > maxDateToResetePassword:
                tokenChangePassword.delete()
                return Response({"msg": "The token has expired"},
                status=HTTP_400_BAD_REQUEST)
            
            tokenChangePassword.delete()
            user.set_password(password)
            user.save()
            return Response({"msg": "Password change successful"},
                status=HTTP_200_OK)
        except:
            return Response({"msg": "The token is incorrect"},
                status=HTTP_400_BAD_REQUEST)

class ChangePasswordApi(APIView):
    permission_classes = (IsAuthenticated,)
    
    @checkParamsJson(listParams=['password'])
    @checkPermissions(permission=regular_code)
    def post(self, request):
        password = request.data['password']

        user = get_user_from_request(self, request)
        user.set_password(password)
        user.save()

        return Response({"msg": "Password change successful"},
                status=HTTP_200_OK)


class TestApi(APIView):
    permission_classes = (IsAuthenticated,)
    
    @checkParamsJson(listParams=['test'])
    @checkPermissions(permission=regular_code)
    def post(self, request):
        test = request.data['test']

        user = get_user_from_request(self, request)

        return Response({"msg": f"hello {user.username}, {test}"},
                status=HTTP_200_OK)

class ChangePermission(APIView):
    permission_classes = (IsAuthenticated,)
    
    @checkParamsJson(listParams=['username', 'permission'])
    @checkPermissions(permission=PermissionsCode['super_manager_code'])
    def post(self, request):
        username = request.data['username']
        permission = request.data['permission']
        user = get_user_from_request(self, request)

        try:
            userToChange = User.objects.get(username=username)
        except:
            return Response({"msg": 'The user does not exist'}, status=HTTP_400_BAD_REQUEST)
        
        last_permission = userToChange.profile.permission
        
        if last_permission >= user.profile.permission:
            return Response({"msg": 'Permission is required'}, status=HTTP_403_FORBIDDEN)

        userToChange.permission = permission
        userToChange.save()

        data = f"change permission {last_permission} -> {permission}, by {user.username}"

        system_message = SystemMessage.create(user=user, data=data, permission=PermissionsCode['inspector_code'])
        system_message.save()
        
        system_messages = user.profile.system_messages
        system_messages.add(system_message)
        system_messages.save()


        return Response({"msg": f"{userToChange.username} became {PermissionsCode['super_manager_code']}"},
                status=HTTP_200_OK)


class GetListMailbox(APIView):
    permission_classes = (IsAuthenticated,)
    
    @checkParamsJson(listParams=[])
    @checkPermissions(permission=regular_code)
    def post(self, request):
        user = get_user_from_request(self, request)
        mailboxesJson = user.profile.getAllHeadMailbox()

        return Response({"msg": mailboxesJson},
                status=HTTP_200_OK)

class GetMailbox(APIView):
    permission_classes = (IsAuthenticated,)
    
    @checkParamsJson(listParams=['id'])
    @checkPermissions(permission=regular_code)
    def post(self, request):

        idMailbox = request.data['id']
        user = get_user_from_request(self, request)
        mailboxes = user.profile.mailboxes
        mailbox = mailboxes.get(mailbox_id=idMailbox)
        mailboxJson = mailbox.getMailbox()

        return Response({"msg": mailboxJson},
                status=HTTP_200_OK)


class SendPrivateMessage(APIView):
    permission_classes = (IsAuthenticated,)
    
    @checkParamsJson(listParams=['data', 'id'])
    @checkPermissions(permission=regular_code)
    def post(self, request):
        
        idMailbox = request.data['id']
        dataMessage = request.data['data']

        user = get_user_from_request(self, request)

        mailboxes = user.profile.mailboxes
        mailbox = mailboxes.get(mailbox_id=idMailbox)

        newMessage = PrivateMessage.create(user=user, data=dataMessage, permission=regular_code, addressee=mailbox.other_user)
        newMessage.save()

        mailboxes.sendMessage(newMessage)

        return Response({"msg": newMessage.getMessage()},
                status=HTTP_200_OK)


class GetListMessagesUser(APIView):
    permission_classes = (IsAuthenticated,)
    
    @checkParamsJson(listParams=['username'])
    @checkPermissions(permission=regular_code)
    def post(self, request):
        
        username = request.data['username']

        try:
            user = User.objects.get(username=username)
        except:
            return Response({"msg": 'The user does not exist'}, status=HTTP_400_BAD_REQUEST)
        
        myUser = get_user_from_request(self, request)
        listMessages = user.profile.getAllMessages(myUser.profile.permission)
        return Response({"msg": listMessages},
                status=HTTP_200_OK)

class GetListPostsUser(APIView):
    permission_classes = (IsAuthenticated,)
    
    @checkParamsJson(listParams=['username'])
    @checkPermissions(permission=regular_code)
    def post(self, request):
        
        username = request.data['username']

        try:
            user = User.objects.get(username=username)
        except:
            return Response({"msg": 'The user does not exist'}, status=HTTP_400_BAD_REQUEST)
        
        myUser = get_user_from_request(self, request)
        listPosts = user.profile.getAllPosts(myUser.profile.permission)
        return Response({"msg": listPosts},
                status=HTTP_200_OK)


class GetSystemMessages(APIView):
    permission_classes = (IsAuthenticated,)
    
    @checkParamsJson(listParams=['username'])
    @checkPermissions(permission=inspector_code)
    def post(self, request):
        
        username = request.data['username']

        try:
            user = User.objects.get(username=username)
        except:
            return Response({"msg": 'The user does not exist'}, status=HTTP_400_BAD_REQUEST)
        
        myUser = get_user_from_request(self, request)
        if myUser.profile.permission <= user.permission:
            return Response({"msg": 'Permission is required'}, status=HTTP_403_FORBIDDEN)
        
        listPosts = user.profile.getAllSystemMessage(myUser.profile.permission)
        return Response({"msg": listPosts},
                status=HTTP_200_OK)

class GetUsername(APIView):
    permission_classes = (IsAuthenticated,)
    
    @checkParamsJson(listParams=[])
    @checkPermissions(permission=regular_code)
    def post(self, request):
        user = get_user_from_request(self, request)

        return Response({"username": user.username, 'permission': user.profile.permission},
                status=HTTP_200_OK)