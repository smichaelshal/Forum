from django.contrib import admin
from .models.message import Message, HistoryMessage
from .models.post import Post
from .models.forum import Forum
from .models.category import Category
from .models.system_message import SystemMessage
from .models.private_message import PrivateMessage


admin.site.register(HistoryMessage)
admin.site.register(Message)
admin.site.register(Post)
admin.site.register(Forum)
admin.site.register(Category)
admin.site.register(SystemMessage)
admin.site.register(PrivateMessage)
