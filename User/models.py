from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class UsersManager(BaseUserManager):
    def create_user(self, id_number, password=None, **extra_fields):
        if not id_number:
            raise ValueError('The ID Number must be set')
        user = self.model(id_number=id_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, id_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(id_number, password, **extra_fields)


class Role(models.Model):
    role_name = models.CharField(max_length=50)

    def __str__(self): return self.role_name


class Users(AbstractUser):
    id_number = models.CharField(max_length=20, unique=True)
    username = models.CharField(max_length=150, unique=False, null=True, blank=True)
    school_email = models.EmailField(unique=True, null=True, blank=True)

    USERNAME_FIELD = 'id_number'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)
    phone = models.CharField(max_length=15, blank=True, null=True)

    objects = UsersManager()

    def __str__(self):
        return self.id_number