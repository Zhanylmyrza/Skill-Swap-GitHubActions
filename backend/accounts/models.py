from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)


class UserAccountManager(BaseUserManager):
    def create_user(self, email, full_name, password=None):
        if not email:
            raise ValueError("Users must have an email address")

        email = self.normalize_email(email)
        user = self.model(email=email, full_name=full_name)

        user.set_password(password)
        user.save()

        return user


class UserAccount(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(max_length=255, unique=True)
    full_name = models.CharField(max_length=400)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    image = models.ImageField(null=True, upload_to="images/")
    job_title = models.CharField(max_length=400, null=True, blank=True)
    education = models.CharField(max_length=800, null=True, blank=True)
    experience = models.TextField(null=True, blank=True)
    skills = models.TextField(null=True, blank=True)
    can_ask_for_help = models.BooleanField(default=False)
    free_times = models.CharField(max_length=800, null=True, blank=True)
    cost_of_mentoring = models.IntegerField(null=True, blank=True, default=0)
    currency = models.CharField(max_length=400, default="USD")
    saved_persons = models.ManyToManyField("self", symmetrical=False, blank=True)
    is_online = models.BooleanField(default=False)

    objects = UserAccountManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "full_name",
    ]

    def get_full_name(self):
        return self.full_name

    def __str__(self):
        return self.email
