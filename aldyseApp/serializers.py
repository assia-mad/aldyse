from django.utils import timezone
from dj_rest_auth.registration.serializers import RegisterSerializer 
from dj_rest_auth.serializers import LoginSerializer , UserDetailsSerializer
from rest_framework import serializers
from .models import *
from .adapter import *
from django.conf import settings
from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist
from datetime import timedelta
from decimal import Decimal
import random

class BoutiqueSerializer(serializers.ModelSerializer):
    class Meta :
        model = Boutique
        fields = ['id','owner','name','wilaya','gps_address','is_free','is_certified','commercial_register']

class ListBoutiqueSerializer(serializers.ModelSerializer):
    class Meta :
        model = Boutique
        fields = ['id','name']

class CustomRegisterSerializer(RegisterSerializer):
    username = None
    first_name = serializers.CharField(required = True , write_only = True)
    last_name = serializers.CharField(required = True , write_only = True)
    email = serializers.EmailField(required = True)
    wilaya = serializers.CharField(max_length=100 ,required = True)
    commune = serializers.CharField(max_length=100 ,required = True)
    tel = serializers.CharField(max_length=10 , validators=[num_only], required = True)
    age = serializers.IntegerField(min_value = 10)
    role = serializers.ChoiceField(choices=role_choices)
    gender = serializers.ChoiceField(choices= gender_choices)
    password1 = serializers.CharField( write_only=True, required=True, style={'input_type': 'password', })
    password2 = serializers.CharField( write_only=True, required=True, style={'input_type': 'password', })
    is_active = serializers.BooleanField(default=True)
    boutique = BoutiqueSerializer(required = False , allow_null = True )
    def get_cleaned_data(self):
        data_dict = super().get_cleaned_data()
        data_dict['first_name'] = self.validated_data.get('first_name', '')
        data_dict['last_name'] = self.validated_data.get('last_name', '')
        data_dict['wilaya'] = self.validated_data.get('wilaya', '')
        data_dict['commune'] = self.validated_data.get('commune', '')
        data_dict['tel'] = self.validated_data.get('tel', '')
        data_dict['age'] = self.validated_data.get('age', '')
        data_dict['role'] = self.validated_data.get('role', '')
        data_dict['gender'] = self.validated_data.get('gender', '')
        data_dict['is_active'] = self.validated_data.get('is_active', '')
        return data_dict
    def save(self, request):
        user = super().save(request)
        Favorite = FavoriteList.objects.create(owner = user)
        try:
            boutique = self._validated_data['boutique'] or None
            name = boutique.get('name')
            gps_address = boutique.get('gps_address')
            commercial_register = boutique.get('commercial_register')
            is_free = boutique.get('is_free')
            is_certified = boutique.get('is_certified')
            Boutique.objects.create(owner = user,name = name,gps_address = gps_address,is_free=is_free,is_certified=is_certified,commercial_register=commercial_register) 
            return user
        except :
            return user
        

class CustomLoginSerializer(LoginSerializer): 
    username = None

class CustomUserDetailSerializer(UserDetailsSerializer):
    wilaya = serializers.CharField(max_length=100 )
    commune = serializers.CharField(max_length=100)
    tel = serializers.CharField(max_length=10 , validators=[num_only])
    image = serializers.ImageField(allow_null=True)
    role = serializers.ChoiceField(choices= role_choices)
    age = serializers.IntegerField(min_value = 10)
    gender = serializers.ChoiceField(choices= gender_choices)
    
    class Meta : 
        model = User
        fields = ['id','first_name','last_name','email','wilaya','commune','tel','image','role','age','gender','is_staff', 'is_active','otp']

class ManageusersSerializer(serializers.ModelSerializer):
    class Meta :
        model = User
        fields = ['id','first_name','last_name','email','wilaya','commune','tel','image','role','age','gender','is_staff', 'is_active','otp']

class UpdateUsersByAdminSerializer(serializers.Serializer):
    role  = serializers.ChoiceField(choices=role_choices , default=role_choices[1])
    is_active = serializers.BooleanField( default=True)
        
    def update(self, instance, validated_data):
        new_role = validated_data.get('role') 
        if instance.role != new_role:
            subject = 'Role changer'
            message = f'Salut {instance.first_name} {instance.last_name} votre role a été changer à {new_role}. svp déconnectez vous et connectez encore pour pouvoir accédez a vos nouvelles fonctionnalités'
            from_email = settings.EMAIL_HOST_USER 
            recipient_list = [instance.email]
            send_mail(subject, message,from_email,recipient_list , fail_silently=False)
        if validated_data.get('role') == 'Admin' :
            instance.is_staff = True
        if validated_data.get('role') != 'Admin':
            instance.is_staff= False
        instance.role = validated_data.get('role', instance.role)
            
        if instance.is_active != validated_data.get('is_active'):
            if validated_data.get('is_active') == True:
                account = 'est activé'
            else :
                account = 'est désactivé'
            subject = 'Compte Aldyse'
            message = f'Salut {instance.first_name} {instance.last_name} votre compte {account}'
            from_email = settings.EMAIL_HOST_USER 
            recipient_list = [instance.email]
            send_mail(subject, message,from_email,recipient_list , fail_silently=False)      
        instance.is_active = validated_data.get('is_active', instance.is_active)
        try:
            instance.user.auth_token.delete()
        except (AttributeError, ObjectDoesNotExist):
            pass    
        instance.save()
        return instance 

class TypeSerializer(serializers.ModelSerializer):
    class Meta :
        model = Type
        fields = ['id','name','image']

class CategorySerializer(serializers.ModelSerializer):
    class Meta :
        model = Category
        fields = ['id','name','image']

class SubcategorySerializer(serializers.ModelSerializer):
    class Meta :
        model = SubCategory
        fields = ['id','name','category','image']

class CertificateDemandSerializer(serializers.ModelSerializer):
    class Meta :
        model = CertificateDemand
        fields = ['id','boutique','demand','image','is_accepted','created_at']
    
    def update(self, instance, validated_data):
        if validated_data.get('is_accepted') == True:
            boutique = instance.boutique
            boutique.is_certified = True
            boutique.save()
        return super().update(instance, validated_data)

class ListDetailserializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','email']

class ColorSerializer(serializers.ModelSerializer):
    class Meta :
        model = Color
        fields = ['id','code']

class SizeSerializer(serializers.ModelSerializer):
    class Meta :
        model = Size
        fields = ['id','code']

class SizeTypeSerializer(serializers.ModelSerializer):
    class Meta :
        model = SizeType
        fields = ['id','name']

class ImageSerializer(serializers.ModelSerializer):
    class Meta :
        model = ProductImage
        fields = ['image','product']

class ProductSerializer(serializers.ModelSerializer):
    available_colors = serializers.SlugRelatedField(many=True, slug_field='code', read_only=True)
    update_available_colors= serializers.ListField(
        child=serializers.CharField(max_length=50), write_only=True , required = False)
    available_sizes = serializers.SlugRelatedField(many=True, slug_field='code', read_only=True)
    update_available_sizes = serializers.ListField(
        child=serializers.CharField(max_length=50), write_only=True , required = False)
    # images= ImageSerializer(many=True, read_only = True, required = False)
    # uploaded_images = serializers.ListField ( child = serializers.FileField(max_length = 1000000, allow_empty_file =True, use_url = False) , write_only = True )
    class Meta :
        model = Product
        fields = ['id','boutique','name','description','price','discount_percentage','gender','product_type','sub_category','available_colors','update_available_colors','size_type','available_sizes','update_available_sizes','published_by','happyhour_discount','created_at']
    
    def create(self, validated_data):
        boutique = validated_data.get('boutique')
        name= validated_data.get('name')
        description = validated_data.get('description')
        price = validated_data.get('price')
        discount_percentage = validated_data.get('discount_percentage')
        gender = validated_data.get('gender')
        product_type = validated_data.get('product_type')
        sub_category = validated_data.get('sub_category')
        size_type = validated_data.get('size_type')
        published_by = validated_data.get('published_by')
        new_product = Product.objects.create(boutique=boutique, name=name, description=description, price=price, discount_percentage=discount_percentage, gender=gender, product_type=product_type, sub_category=sub_category, size_type=size_type, published_by=published_by)
        sizes_codes = validated_data.pop('update_available_sizes',[])
        sizes = []
        colors_codes = validated_data.pop('update_available_colors',[])
        colors = []
        # uploaded_data = validated_data.pop('uploaded_images',[])
        # for uploaded_item in uploaded_data:
        #     new_product_image = ProductImage.objects.create(product = new_product, image = uploaded_item)
        for code in sizes_codes:
            size, created = Size.objects.get_or_create(code = code)
            sizes.append(size)
        for code in colors_codes:
            color, created = Color.objects.get_or_create(code = code)
            colors.append(color)
        new_product.available_sizes.set(sizes)
        new_product.available_colors.set(colors)
        new_product.save()
        return new_product

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        sizes_codes = validated_data.pop('update_available_sizes',[])  
        print(sizes_codes)
        sizes = []
        colors_codes = validated_data.pop('update_available_colors',[]) 
        colors = []
        for code in sizes_codes:
            size, created = Size.objects.get_or_create(code = code)
            sizes.append(size)
        for code in colors_codes:
            color, created = Color.objects.get_or_create(code = code)
            colors.append(color)
        # try:
        #     uploaded_data = validated_data.pop('uploaded_images',[])
        #     for uploaded_item in uploaded_data:
        #         new_product_image = ProductImage.objects.create(product = instance, image = uploaded_item)
        # except:
        #     pass
        instance.available_sizes.set(sizes)
        instance.available_colors.set(colors)
        instance.save()
        return instance
   

class OrderSerializer(serializers.ModelSerializer):
    class Meta :
        model = Order
        fields = ['id','owner','panier','product','color','size','quantity','price','created_at']

class PanierSerializer(serializers.ModelSerializer):
    orders= serializers.PrimaryKeyRelatedField(many=True , queryset=Order.objects.filter(panier__isnull = True))
    class Meta :
        model = Panier
        fields = ['id','owner','wilaya','commune','detailed_place','company','postal_code','tel','home_delivery','orders','state','total_price','delivery_price','created_at']
    def create(self, validated_data):
        orders = validated_data.pop('orders')
        panier = super().create(validated_data)
        for order in orders:
            order.panier = panier
            order.save()
        return panier

    def update(self, instance, validated_data):
        new_panier = super().update(instance, validated_data)
        if new_panier.state == "annulé":
            owner = new_panier.owner
            num_panier_annule = Panier.objects.filter(owner = owner , state='annulé').count()
            name = owner.first_name+' '+owner.last_name
            if num_panier_annule < 3 :
                subject = 'Avertissement'
                message = f'Bonjour {name} hadi machi affsa tae rjal ya kho'
                from_email = settings.EMAIL_HOST_USER 
                recipient_list = [owner.email]
                send_mail(subject, message,from_email,recipient_list , fail_silently=False)
            else :
                owner.is_active = False
                subject = 'Compte Aldyse'
                message = f'Bonjour {name} votre compte a été désactivé'
                from_email = settings.EMAIL_HOST_USER 
                recipient_list = [owner.email]
                send_mail(subject, message,from_email,recipient_list , fail_silently=False) 
        return new_panier
    
class NonValidatedBoutiqueSerializer(serializers.ModelSerializer):
    class Meta :
        model = Boutique
        fields = ['id','owner','name','is_free','commercial_register']

class FavoritListSerializer(serializers.ModelSerializer):
    products = serializers.PrimaryKeyRelatedField(
        queryset= Product.objects.all(),
        many=True,
        required=False
    )
    class Meta:
        model = FavoriteList
        fields = ['id','owner','products']

class HappyHourSerializer(serializers.ModelSerializer):
    modified_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M")
    class Meta:
        model = HappyHour
        fields = ['id','discount_percentage','boutiques','is_active','modified_at']

class PasswordrestSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email']

class PasswordResetConfirmSerializer(serializers.ModelSerializer):
    new_password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password', })
    new_password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password', })
    class Meta:
        model = User
        fields = ['otp','email','new_password','new_password2']

class WilayaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wilaya
        fields = ['id','name']

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id','name','image','manager']

class DestinationSerializer(serializers.ModelSerializer):
    class Meta :
        model = Destination
        fields = ['id','depart','company','destination','desk_price','home_price','return_costs']

class PublicitySerializer(serializers.ModelSerializer):
    class Meta :
        model = Publicity
        fields = ['id','title','description','image']

class SignalSerializer(serializers.ModelSerializer):
    class Meta :
        model = Signal
        fields = ['id','user','description','image']

class JustificationSerializer(serializers.ModelSerializer):
    class Meta :
        model = Signal
        fields = ['id','user','panier','description']
