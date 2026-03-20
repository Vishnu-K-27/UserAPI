from django.db import models
from django.contrib.auth.models import AbstractUser
class User(AbstractUser):
    username=None
    name = models.CharField(max_length=100)

    email = models.EmailField(unique=True)

    password = models.CharField(max_length=255)

    is_delete = models.BooleanField(default=False)
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    class Meta:
        app_label = 'users_app'