from django.urls import path
from .views import (
    GetCategory,
    GetForum,
    GetPost,
    CreateCategory,
    CreateForum,
    CreatePost,
    CreateMessage,
    GetListCategories,
    )


urlpatterns = [
    path('get_category/', GetCategory.as_view(), name='get_category'),
    path('get_forum/', GetForum.as_view(), name='get_forum'),
    path('get_post/', GetPost.as_view(), name='get_post'),
    path('get_list_categories/', GetListCategories.as_view(), name='get_list_categories'),
    
    path('create_category/', CreateCategory.as_view(), name='create_category'),
    path('create_forum/', CreateForum.as_view(), name='create_forum'),
    path('create_post/', CreatePost.as_view(), name='create_post'),
    path('create_message/', CreateMessage.as_view(), name='create_message'),
]