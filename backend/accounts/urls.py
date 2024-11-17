from django.urls import path

from .views import PersonDetailView, PersonListView, AddToLikedView, RemoveFromLikedView

urlpatterns = [
    path("<str:pk>", PersonDetailView.as_view(), name="person_detail"),
    path("<str:email>/like", AddToLikedView.as_view(), name="like_person"),
    path("<str:email>/unlike", RemoveFromLikedView.as_view(), name="unlike_person"),
    path("", PersonListView.as_view(), name="persons"),
]
