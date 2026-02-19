from django.db import models
from django.contrib.auth.models import AbstractUser
# from django.settings import User


class CustomUser(AbstractUser):
    bio = models.TextField()
    profile_picture = models.ImageField(upload_to='uploads/profile_picture/')
    following = models.ManyToManyField(
        "self",
        symmetrical=False,
        related_name="followers",
        blank=True
    )


