from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
# Create your models here.


class CustomUserManager(BaseUserManager):
    use_in_migrations=True

    def create_user(self,email,password=None,**extra_fields):
        if not email:
            raise ValueError('The email must be set')
        email=self.normalize_email(email)
        user=self.model(email=email,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self,email,password=None,**extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        extra_fields.setdefault('is_active',True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')
        
        return self.create_user(email,password,**extra_fields)

class User(AbstractBaseUser,PermissionsMixin):
    email=models.EmailField(unique=True)
    first_name=models.CharField(max_length=200,blank=True)
    last_name=models.CharField(max_length=200,blank=True)
    is_staff=models.BooleanField(default=False)
    is_active=models.BooleanField(default=True)
    date_joined=models.DateTimeField(auto_now_add=True)
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=[]

    objects=CustomUserManager()

    def __str__(self):
        return self.email
    
    class Meta():
        db_table='customuser'

class Client(models.Model):
    name=models.CharField(max_length=200)
    email=models.EmailField()
    phone_number=models.CharField(max_length=15)

    def __str__(self):
        return self.name
    
    class Meta():
        db_table='client'

class Consultants(models.Model):
    service=models.CharField(max_length=200,blank=True,null=True)
    purpose=models.TextField()
    status=models.CharField(max_length=100)
    consult_time=models.DateTimeField()
    # duration=models.DurationField(null=True,blank=True)
    owner=models.ForeignKey(Client,related_name='appointments',on_delete=models.CASCADE)

    def __str__(self):
        return self.purpose
    
    class Meta():
        db_table='consultants'
