from email.policy import default
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.utils import timezone

num_only = RegexValidator(r'^[0-9]*$','only numbers are allowed')

role_choices = [ 
    ('Admin','Admin'),
    ('Visiteur','Visiteur'),
    ('Vendeur','Vendeur'),
    ('Livreur','Livreur')
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

panier_state_choices = [
    ('livré','livré'),
    ('non livré','non livré'),
]

class User(AbstractUser):
    wilaya = models.CharField(max_length=100 , blank=True , null= True)
    commune = models.CharField(max_length=100 , blank=True , null= True)
    tel = models.CharField(max_length=10 , validators=[num_only],blank=True)
    image = models.ImageField(upload_to='profile_images/', blank = True , null = True , verbose_name='user_img')
    role =  models.CharField(max_length=30 , choices=role_choices)
    age = models.PositiveIntegerField(blank=True , null= True)
    gender =  models.CharField(max_length=30 , choices=gender_choices,null = True)
    otp = models.CharField(max_length=6, null=True, blank=True)

class Wilaya(models.Model):
    name = models.CharField(max_length=30 , blank= False , null = False)
    def __str__(self):
        return self.name

class Company(models.Model):
    name = models.CharField(max_length=30,unique=True)
    departs = models.ManyToManyField(Wilaya ,related_name='departs' )
    manager = models.OneToOneField(User , related_name='company', on_delete=models.SET_NULL , null = True)
    def __str__(self):
        return self.name

class Destination(models.Model):
    depart = models.ForeignKey(Wilaya , related_name='wilaya_depart', on_delete= models.CASCADE)
    company = models.ForeignKey(Company, related_name='destination', on_delete=models.CASCADE)
    destination = models.ForeignKey(Wilaya ,related_name='destination',on_delete=models.CASCADE , null=True)#make it not null later
    desk_price = models.PositiveIntegerField()
    home_price = models.PositiveIntegerField()
    return_costs = models.PositiveIntegerField()
    def __str__(self):
        return self.depart.name+'->'+ self.destination.name

class Boutique(models.Model):
    owner = models.OneToOneField(User , related_name='boutique', on_delete= models.CASCADE , null= True)
    name = models.CharField(max_length=150)
    wilaya = models.ForeignKey(Wilaya , related_name='boutique', on_delete=models.SET_NULL , null = True)
    gps_address = models.CharField(max_length=100)
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
    price = models.PositiveIntegerField()
    discount_percentage = models.DecimalField(decimal_places =2,max_digits = 4,  default= 00.00)
    product_type = models.ForeignKey(Type , related_name='product', on_delete=models.CASCADE)
    size_type =  models.ForeignKey(SizeType , related_name='product', on_delete=models.CASCADE,null=True)#remove null after  french italien
    sub_category = models.ForeignKey(SubCategory , related_name='product', on_delete=models.CASCADE)
    available_colors = models.ManyToManyField(Color , related_name='product_colours')
    available_sizes = models.ManyToManyField(Size , related_name='product_sizes')
    gender = models.CharField(max_length=50,choices=product_gender_choices,default='mixte')
    published_by = models.CharField(max_length=50,choices=product_origins_choices, default ='Aldyse')
    happyhour_discount = models.BooleanField(default = False)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name= 'product_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to = 'product_images/', blank = False , null= False)
    def __str__(self):
        return self.image.url

class FavoriteList(models.Model):
    owner = models.OneToOneField(User , related_name='Favoritelist', on_delete= models.CASCADE)
    products = models.ManyToManyField(Product , related_name='favorite_products')

class HappyHour(models.Model):
    discount_percentage = models.DecimalField(decimal_places =2,max_digits = 4)
    boutiques = models.ManyToManyField(Boutique, related_name='Happy_hours')
    is_active = models.BooleanField(default=False)
    modified_at = models.DateTimeField(default= timezone.now)

class Panier(models.Model):
    owner = models.ForeignKey(User , related_name='panier',on_delete= models.CASCADE)
    detailed_place = models.CharField(max_length=150 , blank= False , null= False)
    wilaya = models.ForeignKey(Wilaya, related_name='panier',on_delete=models.SET_NULL , null = True)#make it not null
    company = models.ForeignKey(Company , related_name='paniers',on_delete = models.SET_NULL , null = True)#make it not null
    commune = models.CharField(max_length=50 , blank= False , null= False)
    postal_code = models.PositiveIntegerField()
    tel = models.CharField(max_length=10 , validators=[num_only], blank= True , null= True)
    total_price = models.DecimalField(max_digits=8, decimal_places=2 ,default=0.0)
    state = models.CharField(max_length=20 , choices=panier_state_choices, default = 'non livré')
    home_delivery = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class Order(models.Model):
    owner = models.ForeignKey(User , related_name='orders', on_delete= models.CASCADE , null=True)
    panier = models.ForeignKey(Panier , related_name='orders',on_delete= models.CASCADE , null= True)
    product = models.ForeignKey(Product , related_name='product_ordered',on_delete=models.CASCADE)
    color = models.CharField(max_length=7 , blank=False , null = False)
    size = models.CharField(max_length=10 , blank= False , null = False)
    quantity = models.PositiveIntegerField(default = 1)
    created_at = models.DateTimeField(auto_now_add=True)

class Publicity(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    image = models.ImageField(upload_to = 'pub_images/', blank = True, null= True)