from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Login(models.Model):
    username = models.CharField(max_length=128)
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.username

class Utang(models.Model):
    name = models.CharField(max_length=128)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    email = models.EmailField(max_length=128)
    date = models.DateField(auto_now_add=True)
    isUtangToUser = models.BooleanField(default=True)

    utangs = models.ManyToManyField(User, related_name='utangs')

    def __str__(self):
        return self.name  