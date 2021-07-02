from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager
from django.core.validators import RegexValidator
from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
from random import randint
from django.contrib.auth.hashers import make_password
# Create your models here.


class User(AbstractUser):
    mobile_no = models.CharField(verbose_name='mobile',unique=True,validators=[
        RegexValidator(
            regex='[1-9]{1}[0-9]{9}',
            message='Number should be 10 digit',
            code='invalid_number'
        ),
    ], max_length=10, default='1234567890')
    otp = models.CharField(max_length=6,blank=True,null=True)


    def __str__(self):
        return self.mobile_no


class Company(models.Model):
    name = models.CharField(max_length=200,blank=True,null=True)

    def __str__(self):
        return self.name


def user_directory_path(instance,filename):
    return f'chicken/{filename}'


class Chicken(models.Model):
    name = models.CharField(max_length=200,blank=True,null=True)
    company = models.ForeignKey(Company,blank=True,null=True,on_delete=models.CASCADE,related_name="comp")
    image = models.ImageField(upload_to=user_directory_path,blank=True,null=True)
    price = models.PositiveSmallIntegerField(default=0)
    ratings = models.FloatField(default=0)
    fresh=models.BooleanField(default=True)
    approx_time = models.PositiveSmallIntegerField(default=30)
    description = models.TextField(blank=True,null=True)
    liver = models.BooleanField(default=True)
    intestine = models.BooleanField(default=True)
    skin = models.BooleanField(default=True)
    def __str__(self):
        return self.name

class OrderType(models.Model):
    pass



@receiver(post_save,sender=User)
def userprofile_receiver(sender, instance, created, *args, **kwargs):
    if created:
        if not instance.is_superuser:
            u = User.objects.get(pk=instance.id)
            u.set_password('1234')
            u.username = instance.mobile_no
            u.save()

