from dj_rest_auth.registration.serializers import RegisterSerializer 
from dj_rest_auth.serializers import LoginSerializer , UserDetailsSerializer
from rest_framework import serializers
from .models import *
from .adapter import *
from django.conf import settings
from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist

class BoutiqueSerializer(serializers.ModelSerializer):
    class Meta :
        model = Boutique
        fields = ['id','owner','name','gps_address','is_free','is_certified','commercial_register']

class CustomRegisterSerializer(RegisterSerializer):
    username = None
    first_name = serializers.CharField(required = True , write_only = True)
    last_name = serializers.CharField(required = True , write_only = True)
    email = serializers.EmailField(required = True)
    wilaya = serializers.CharField(max_length=100 ,required = True)
    commune = serializers.CharField(max_length=100 ,required = True)
    tel = serializers.CharField(max_length=10 , validators=[num_only], required = True)
    age = serializers.IntegerField(min_value = 10)
    password1 = serializers.CharField( write_only=True, required=True, style={'input_type': 'password', })
    password2 = serializers.CharField( write_only=True, required=True, style={'input_type': 'password', })
    boutique = BoutiqueSerializer(required = False , allow_null = True )
    def get_cleaned_data(self):
        data_dict = super().get_cleaned_data()
        data_dict['first_name'] = self.validated_data.get('first_name', '')
        data_dict['last_name'] = self.validated_data.get('last_name', '')
        data_dict['wilaya'] = self.validated_data.get('wilaya', '')
        data_dict['commune'] = self.validated_data.get('commune', '')
        data_dict['tel'] = self.validated_data.get('tel', '')
        data_dict['age'] = self.validated_data.get('age', '')
        return data_dict
    def save(self, request):
        user = super().save(request)
        try:
            boutique = self._validated_data['boutique'] or None
            name = boutique.get('name')
            owner = boutique.get('owner')
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
    class Meta : 
        model = User
        fields = ['id','first_name','last_name','email','wilaya','commune','tel','image','role','age','is_staff', 'is_active']

class ManageusersSerializer(serializers.ModelSerializer):
    class Meta :
        model = User
        fields = ['id','first_name','last_name','email','wilaya','commune','tel','image','role','age','is_staff', 'is_active']

class UpdateUsersByAdminSerializer(serializers.Serializer):
    role  = serializers.ChoiceField(choices=role_choices , default=role_choices[1])
    is_active = serializers.BooleanField( default=True)
        
    def update(self, instance, validated_data):
        new_role = validated_data.get('role') 
        if instance.role != new_role:
            subject = 'Role changed'
            message = f'Salut {instance.first_name} {instance.last_name} your role has been changed to {new_role} please logout then login again to get your suitable interface'
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
                account = 'has been activated'
            else :
                account = 'has been desactivated'
            subject = 'Aldyse account'
            message = f'Hi {instance.first_name} {instance.last_name} your account {account}'
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