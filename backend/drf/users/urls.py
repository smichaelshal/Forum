from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from .views import (
    RegisterAPI,
    ConfirmedEmailApi,
    LoginApi,
    ResetPasswordApi,
    ChangePasswordApi,

    GetListMailbox,
    GetMailbox,
    SendPrivateMessage,
    ChangePermission,

    GetListPostsUser,
    GetListMessagesUser,
    GetSystemMessages,
    
    GetUsername,
    TestApi,
    )
from rest_framework_simplejwt import views as jwt_views


urlpatterns = [
    path('register/', RegisterAPI.as_view(), name='register'),
    path('test/', TestApi.as_view(), name='test'),
    path('confirmed-email/', ConfirmedEmailApi.as_view(), name='confirmed-email'),
    path('login/', LoginApi.as_view(), name='login'),
    path('reset-password/', ResetPasswordApi.as_view(), name='reset-password'),
    path('change-password/', ChangePasswordApi.as_view(), name='change-password'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    
    path('get-list-mailbox/', GetListMailbox.as_view(), name='get-list-mailbox'),
    path('get-mailbox/', GetMailbox.as_view(), name='get-mailbox'),
    path('send-private-message/', SendPrivateMessage.as_view(), name='send-private-message'),
    path('change-permission/', ChangePermission.as_view(), name='change-permission'),

    path('get-list-posts-user/', GetListPostsUser.as_view(), name='get-list-posts-user'),
    path('get-list-messages-user/', GetListMessagesUser.as_view(), name='get-list-messages-user'),
    path('get-system-messages/', GetSystemMessages.as_view(), name='get-system-messages'),
    
    path('get-username/', GetUsername.as_view(), name='get-username'),
]