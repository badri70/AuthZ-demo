from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    class Roles(models.TextChoices):
        USER = "user", "User"
        MODERATOR = "moderator", "Moderator"
        ADMIN = "admin", "Admin"
    
    role = models.CharField(
        max_length=20,
        choices=Roles.choices,
        default=Roles.USER
    )
