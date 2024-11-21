from rest_framework import views
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import generics
from accounts.models import UserAccount
from accounts.serializers import (
    ProfileSerializer,
    SingleProfileSerializer,
)
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.response import Response
from django.http import HttpRequest


class PersonListView(generics.ListAPIView):
    # queryset = UserAccount.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserAccount.objects.exclude(pk=self.request.user.pk)


class PersonDetailView(generics.RetrieveUpdateAPIView):

    queryset = UserAccount.objects.all()
    serializer_class = SingleProfileSerializer
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser, JSONParser]


class AddToLikedView(views.APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, format=None, *args, **kwargs):

        current_user = request.user

        user_email = self.kwargs["email"]
        try:
            user = UserAccount.objects.get(email=user_email)
            print("user:", user)
        except UserAccount.DoesNotExist:
            return Response(
                status=404, data=f"User with email '{user_email}' does not exist"
            )

        current_user.saved_persons.add(user)
        return Response(status=200)


class RemoveFromLikedView(views.APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request: HttpRequest, format=None, *args, **kwargs):
        """
        Return a list of all users.
        """
        current_user = request.user

        user_email = self.kwargs["email"]

        user = UserAccount.objects.get(email=user_email)

        current_user.saved_person.remove(user)
        return Response(status=200)
