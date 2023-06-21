from django.db import models
from django.contrib.auth.models import AbstractUser , AbstractBaseUser ,PermissionsMixin
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.base_user import BaseUserManager
# Create your models here.
from game.models import Hero


class MyCustomUserManger(BaseUserManager):
    def create_user(self, phone_number, password, **extra_fields):
        if not phone_number:
            raise ValueError('The phone number must be exist')
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, phone_number, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff', True) is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')  
        
        return self.create_user(phone_number, password, **extra_fields)



# Custom user model с помощью AbstractUser
# class User(AbstractUser):
    # email = models.EmailField(unique=True)
    # date_birth = models.DateField(null=True, blank=True)
    # photo = models.ImageField(upload_to='user/%Y/%m/%d', blank=True)
    # phone_number = PhoneNumberField(null=True, blank = True, unique = True)
    # USERNAME_FIELD = 'phone_number'
    # REQUIRED_FIELDS = ['username', 'email']
    # def __str__(self):
    #     return str(self.phone_number)
    

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    chat_id = models.CharField(max_length=255)
    username = models.CharField(max_length=234, unique=True)
    date_birth = models.DateField(null=True, blank=True)
    photo = models.ImageField(upload_to='user/%Y/%m/%d', blank=True)
    phone_number = PhoneNumberField(null=False, blank = False, unique = True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    data_joined = models.DateTimeField(auto_now_add=True)
    balance = models.DecimalField(max_digits=10,decimal_places=2, default=0)
    favourites = models.ManyToManyField(Hero)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['username', 'email', 'chat_id']

    objects = MyCustomUserManger()

    def __str__(self):
        return str(self.phone_number)
    



