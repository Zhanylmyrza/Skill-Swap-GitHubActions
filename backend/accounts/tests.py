from django.test import TestCase
from accounts.models import UserAccount


class UserAccountModelTest(TestCase):
    def setUp(self):
        self.user = UserAccount.objects.create_user(
            email="testuser@example.com", full_name="Test User", password="password123"
        )

    def test_user_creation(self):
        self.assertEqual(self.user.email, "testuser@example.com")
        self.assertEqual(self.user.get_full_name(), "Test User")
        self.assertTrue(self.user.check_password("password123"))

    def test_user_string_representation(self):
        self.assertEqual(str(self.user), "testuser@example.com")


from rest_framework.test import APITestCase
from rest_framework import status
from accounts.models import UserAccount


class PersonListViewTest(APITestCase):
    def setUp(self):
        self.user1 = UserAccount.objects.create_user(
            email="user1@example.com", full_name="User One", password="password123"
        )
        self.user2 = UserAccount.objects.create_user(
            email="user2@example.com", full_name="User Two", password="password123"
        )
        self.client.force_authenticate(user=self.user1)

    def test_get_person_list(self):
        # URL с учетом префикса "person/"
        response = self.client.get("/person/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["email"], "user2@example.com")


class AddToLikedViewTest(APITestCase):
    def setUp(self):
        self.user1 = UserAccount.objects.create_user(
            email="user1@example.com", full_name="User One", password="password123"
        )
        self.user2 = UserAccount.objects.create_user(
            email="user2@example.com", full_name="User Two", password="password123"
        )
        self.client.force_authenticate(user=self.user1)

    def test_add_to_liked(self):
        # URL с учетом префикса "person/"
        response = self.client.get(f"/person/{self.user2.email}/like")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(self.user2, self.user1.saved_persons.all())
