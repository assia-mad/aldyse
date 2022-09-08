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
gender_choices = [
    ('féminin','féminin'),
    ('masculin','masculin'),
]
product_origins_choices = [
    ('BoutiqueAvecRC','BoutiqueAvecRC'),
    ('BoutiqueSansRC','BoutiqueSansRC'),
    ('Aldyse','Aldyse'),
]
product_gender_choices = [
    ('homme','homme'),
    ('femme','femme'),
    ('enfant','enfant'),
    ('mixte','mixte'),
]

class User(AbstractUser):
    wilaya = models.CharField(max_length=100 , blank=True , null= True)
    commune = models.CharField(max_length=100 , blank=True , null= True)
    tel = models.CharField(max_length=10 , validators=[num_only],blank=True)
    image = models.ImageField(upload_to='profile_images/', blank = True , null = True , verbose_name='user_img')
    role =  models.CharField(max_length=30 , choices=role_choices)
    age = models.PositiveIntegerField(blank=True , null= True)
    gender =  models.CharField(max_length=30 , choices=gender_choices,null = True)

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
    created_at = models.DateTimeField(auto_now_add=True , null=True)

class Color(models.Model):
    code = models.CharField(max_length= 50 ,unique=True, blank= False , null = False)
    def __str__(self):
        return self.code

class Size(models.Model):
    code = models.CharField(max_length=50 , unique=True)
    def __str__(self):
        return self.code

class SizeType(models.Model):
    name = models.CharField(max_length=70)
    def __str__(self):
        return self.name

class Product(models.Model):
    boutique = models.ForeignKey(Boutique , related_name='product', on_delete=models.CASCADE)
    name = models.CharField(max_length=100 , blank= False, null= False)
    description = models.TextField(blank=True , null = True)
    price = models.DecimalField(decimal_places =2,max_digits =10 )
    discount_percentage = models.DecimalField(decimal_places =2,max_digits = 3,  default= 0.00)
    product_type = models.ForeignKey(Type , related_name='product', on_delete=models.CASCADE)
    size_type =  models.ForeignKey(SizeType , related_name='product', on_delete=models.CASCADE,null=True)#remove null after  french italien
    sub_category = models.ForeignKey(SubCategory , related_name='product', on_delete=models.CASCADE)
    available_colors = models.ManyToManyField(Color , related_name='product_colours')
    available_sizes = models.ManyToManyField(Size , related_name='product_sizes')
    gender = models.CharField(max_length=50,choices=product_gender_choices,default='mixte')
    published_by = models.CharField(max_length=50,choices=product_origins_choices, default ='Aldyse')
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name= 'product_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to = 'product_images/', blank = False , null= False)
    def __str__(self):
        return self.image.url

class Panier(models.Model):
    owner = models.ForeignKey(User , related_name='panier',on_delete= models.CASCADE)
    detailed_place = models.CharField(max_length=150 , blank= False , null= False)
    wilaya = models.CharField(max_length=50 , blank= False , null= False)
    commune = models.CharField(max_length=50 , blank= False , null= False)
    postal_code = models.PositiveIntegerField()
    tel = models.CharField(max_length=10 , validators=[num_only], blank= True , null= True)
    created_at = models.DateTimeField(auto_now_add=True)

class Order(models.Model):
    owner = models.ForeignKey(User , related_name='orders', on_delete= models.CASCADE , null=True)
    panier = models.ForeignKey(Panier , related_name='orders',on_delete= models.CASCADE , null= True)
    product = models.ForeignKey(Product , related_name='product_ordered',on_delete=models.CASCADE)
    color = models.CharField(max_length=7 , blank=False , null = False)
    size = models.CharField(max_length=10 , blank= False , null = False)
    quantity = models.PositiveIntegerField(default = 1)
    created_at = models.DateTimeField(auto_now_add=True)

class FavoriteList(models.Model):
    owner = models.OneToOneField(User , related_name='Favoritelist', on_delete= models.CASCADE)
    products = models.ManyToManyField(Product , related_name='favorite_products')
