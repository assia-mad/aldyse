from statistics import mode
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

num_only = RegexValidator(r'^[0-9]*$','only numbers are allowed')

role_choices = [ 
    ('Admin','Admin'),
    ('Visiteur','Visiteur'),
    ('Vendeur','Vendeur'),
]

class User(AbstractUser):
    wilaya = models.CharField(max_length=100 , blank=True , null= True)
    commune = models.CharField(max_length=100 , blank=True , null= True)
    tel = models.CharField(max_length=10 , validators=[num_only],blank=True)
    image = models.ImageField(upload_to='profile_images/', blank = True , null = True , verbose_name='user_img')
    role =  models.CharField(max_length=30 , choices=role_choices , default=role_choices[1])
    age = models.PositiveIntegerField(blank=True , null= True)

class Boutique(models.Model):
    owner = models.OneToOneField(User , related_name='boutique', on_delete= models.CASCADE , null= True)
    name = models.CharField(max_length=150)
    gps_address = models.CharField(max_length=100 )
    is_free = models.BooleanField(default=False)
    is_certified = models.BooleanField(default=False)
    commercial_register = models.ImageField(upload_to='register_images/', blank = True , null = True , verbose_name='register_img')
  


