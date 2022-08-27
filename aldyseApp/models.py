from email.mime import image
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
    role =  models.CharField(max_length=30 , choices=role_choices)
    age = models.PositiveIntegerField(blank=True , null= True)

class Boutique(models.Model):
    owner = models.OneToOneField(User , related_name='boutique', on_delete= models.CASCADE , null= True)
    name = models.CharField(max_length=150)
    gps_address = models.CharField(max_length=100 )
    is_free = models.BooleanField(default=False)
    is_certified = models.BooleanField(default=False)
    commercial_register = models.ImageField(upload_to='register_images/', blank = True , null = True , verbose_name='register_img')
    def __str__(self):
        return self.name

class Type(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='type_images/', blank = True , null = True , verbose_name='type_images')
    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='category_images/', blank = True , null = True , verbose_name='category_images')
    def __str__(self):
        return self.name

class SubCategory(models.Model):
    category = models.ForeignKey(Category , related_name='SubCategories',on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='Subcategory_images/', blank = True , null = True , verbose_name='Subcategory_images')
    def __str__(self):
        return self.name

class CertificateDemand(models.Model):
    boutique = models.OneToOneField(Boutique , related_name='certificate_demand', on_delete=models.CASCADE)
    demand = models.TextField()
    image = models.ImageField(upload_to ='certificate_demandes_images/',blank=True , null=True , verbose_name='certificate_demandes_images')
    is_accepted = models.BooleanField(default=False)


