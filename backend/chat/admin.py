from django.contrib import admin
from chat.models import ChatModel, ChatNotification


# Register your models here.
admin.site.register(ChatModel)
admin.site.register(ChatNotification)
