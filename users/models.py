from django.db import models
from uuid import uuid4


# Create your models here.

class Users(models.Model):
    id_users = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    email = models.CharField(unique=True, max_length=100)
    fullName = models.CharField(max_length=100)
    CEP = models.CharField(max_length=8)
    age = models.PositiveIntegerField()
    cellPhone = models.CharField(max_length=11, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
