from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class CustomUser(AbstractUser):
    age = models.PositiveIntegerField()
    address = models.CharField(max_length=120, blank=True, null=True)

    def __str__(self):
        return self.username