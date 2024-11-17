# from django.urls import path

# from . import views

# urlpatterns = [
#     path("", views.index, name="index"),
#     path("<str:room_name>/", views.room, name="room"),
# ]

from django.urls import path

from . import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="home"),
    path("<str:email>/", views.ChatMessagesView.as_view(), name="chat"),
    # path("contacts/", views.MyContactsApiView.as_view(), name="my_contacts"),
]
