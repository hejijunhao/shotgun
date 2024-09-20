from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class AdministratorManager(BaseUserManager):
    def create_user(self, username, password=None):
        if not username:
            raise ValueError("Administrator must have a username")
        user = self.model(username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        user = self.create_user(username, password=password)
        user.is_admin = True
        user.save(using=self._db)
        return user

class Administrator(AbstractBaseUser):
    username = models.CharField(max_length=30, unique=True)
    is_admin = models.BooleanField(default=False)
    
    objects = AdministratorManager()

    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username