from rest_framework import viewsets , generics , status
from .models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticatedOrReadOnly , IsAuthenticated
from rest_framework.filters import SearchFilter , OrderingFilter
from rest_framework.parsers import JSONParser , FormParser , MultiPartParser
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from .pagination import *
from .permissions import *
import random
from datetime import datetime
from django.db.models import Sum


class BoutiqueView(viewsets.ModelViewSet):
    queryset = Boutique.objects.all()
    serializer_class = BoutiqueSerializer
    # permission_classes = 
    filter_backends = [DjangoFilterBackend,OrderingFilter,SearchFilter]
    filter_fields = ['owner','name','gps_address','is_free','is_certified']
    filterset_fields = ['owner','name','gps_address','is_free','is_certified']
    search_fields = ['owner__id','name','gps_address','is_free','is_certified']
    ordering_fields = ['owner','name','gps_address','is_free','is_certified']

# manage users by Admin
class ManageUsersView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = ManageusersSerializer
    pagination_class = CustomPagination
    # permission_classes = [IsAuthenticated]
    parser_classes = [FormParser, JSONParser, MultiPartParser]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ['first_name','last_name','email','wilaya','commune','tel','role','gender','is_superuser', 'is_active']
    filterset_fields = ['first_name','last_name','email','wilaya','commune','tel','role','gender','is_superuser', 'is_active']
    search_fields = ['first_name','last_name','email','wilaya','commune','tel','role','gender','is_superuser', 'is_active']
    ordering_fields = ['first_name','last_name','email','wilaya','commune','tel','role','gender','is_superuser', 'is_active']

    def get_serializer_class(self):
        serializer_class = self.serializer_class
        if self.request.method == 'PUT':
            serializer_class = UpdateUsersByAdminSerializer
        return serializer_class

class TypeView(viewsets.ModelViewSet):
    queryset = Type.objects.all()
    serializer_class = TypeSerializer
    pagination_class = None
    # permission_classes = 
    filter_backends = [DjangoFilterBackend,OrderingFilter,SearchFilter]
    filter_fields = ['name']
    filterset_fields = ['name']
    search_fields = ['name']
    ordering_fields = ['name']

class CategoryView(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = None
    # permission_classes = 
    filter_backends = [DjangoFilterBackend,OrderingFilter,SearchFilter]
    filter_fields = ['name']
    filterset_fields = ['name']
    search_fields = ['name']
    ordering_fields = ['name']

class SubCategoryView(viewsets.ModelViewSet):
    queryset = SubCategory.objects.all()
    serializer_class = SubcategorySerializer
    pagination_class = None
    # permission_classes = 
    filter_backends = [DjangoFilterBackend,OrderingFilter,SearchFilter]
    filter_fields = ['name','category']
    filterset_fields = ['name','category']
    search_fields = ['name','category__id']
    ordering_fields = ['name','category']

class CertificateDemandView(viewsets.ModelViewSet):
    queryset = CertificateDemand.objects.all()
    serializer_class = CertificateDemandSerializer
    pagination_class = CustomPagination
    # permission_classes = 
    filter_backends = [DjangoFilterBackend,OrderingFilter,SearchFilter]
    filter_fields = ['boutique','demand','is_accepted']
    filterset_fields = ['boutique','demand','is_accepted']
    search_fields = ['boutique__id','demand','is_accepted']
    ordering_fields = ['boutique','demand','is_accepted']
 
class ListDetailView(viewsets.ReadOnlyModelViewSet):#return list of emails and ids of users
    serializer_class = ListDetailserializer
    pagination_class = None
    queryset = User.objects.all()
    filter_backends = [DjangoFilterBackend,OrderingFilter,SearchFilter]
    filter_fields = ['email']
    filterset_fields = ['email']
    search_fields = ['email']
    ordering_fields = ['email']

class ColorView(viewsets.ModelViewSet):
    queryset = Color.objects.all()
    serializer_class = ColorSerializer
    pagination_class = None
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ['code']
    search_fields = ['code']
    ordering_fields = ['code']

class SizeView(viewsets.ModelViewSet):
    queryset = Size.objects.all()
    serializer_class =SizeSerializer
    pagination_class = None
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ['code']
    search_fields = ['code']
    ordering_fields = ['code']

class SizeTypeView(viewsets.ModelViewSet):
    queryset = SizeType.objects.all()
    serializer_class =SizeTypeSerializer
    pagination_class = None
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ['name']
    search_fields = ['name']
    ordering_fields = ['name']

class ProductImageView(viewsets.ModelViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ImageSerializer
    # permission_classes = [IsAuthenticated , AdminOrownerPermission]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    pagination_class = None
    filter_fields = ['product']
    filterset_fields = ['product']
    search_fields = ['product__id']
    ordering_fields = ['product']

class ProductView(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class =ProductSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ['boutique','name','price','discount_percentage','gender','product_type','sub_category','available_colors','size_type','available_sizes','published_by']
    filterset_fields = ['boutique','name','price','discount_percentage','gender','product_type','sub_category','available_colors','size_type','available_sizes','published_by']
    search_fields = ['boutique__id','name','price','discount_percentage','gender','product_type__id','sub_category__id','available_colors__id','size_type__id','available_sizes__id','published_by']
    ordering_fields = ['boutique','name','price','discount_percentage','gender','product_type','sub_category','available_colors','size_type','available_sizes','published_by']

class OrderView(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    pagination_class = None
    # permission_classes = [IsAuthenticated , AdminOrownerPermission]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ['owner','panier','product','color','size','quantity','created_at']
    filterset_fields = ['owner','panier','product','color','size','quantity','created_at']
    search_fields = ['owner__id','panier__id','product__id','color','size','quantity','created_at']
    ordering_fields = ['owner','panier','product','color','size','state','wishlist','qte','created_at']

class PanierView(viewsets.ModelViewSet):
    queryset = Panier.objects.all()
    serializer_class = PanierSerializer
    # permission_classes = [IsAuthenticated , AdminOrownerPermission]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ['owner','detailed_place','wilaya','commune','postal_code','tel','orders','company','state','created_at']
    filterset_fields = ['owner','detailed_place','wilaya','commune','postal_code','tel','orders','company','state','created_at']
    search_fields = ['owner','detailed_place','wilaya','commune','postal_code','tel','orders__id','company','state','created_at']
    ordering_fields = ['owner','detailed_place','wilaya','commune','postal_code','tel','orders','company','state','created_at']

class NonValidatedBoutiqueView(viewsets.ModelViewSet):
    queryset = Boutique.objects.filter(is_free=False ,owner__is_active = False)
    serializer_class = NonValidatedBoutiqueSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ['owner','name','is_free']
    search_fields = ['owner__id','name','is_free']
    ordering_fields = ['owner','name','is_free']

class ProductCategoryList(generics.ListAPIView):
    serializer_class = ProductSerializer
    def get_queryset(self):
        name = self.kwargs['name']
        return Product.objects.filter(sub_category__category__name=name)

class FavoriteListView(viewsets.ModelViewSet):
    queryset = FavoriteList.objects.all()
    serializer_class = FavoritListSerializer
    pagination_class = None
    # permission_classes = [IsAuthenticatedAndOwner]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ['owner','products']
    filterset_fields = ['owner','products']
    search_fields = ['owner__id','products']
    ordering_fields = ['owner','products']

class HappyHourView(viewsets.ModelViewSet):
    queryset = HappyHour.objects.all()
    serializer_class = HappyHourSerializer
    pagination_class = None
    # permission_classes = [IsAuthenticatedAndOwner]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ['discount_percentage','is_active','modified_at']
    filterset_fields = ['discount_percentage','is_active','modified_at']
    search_fields = ['discount_percentage','is_active','modified_at']
    ordering_fields = ['discount_percentage','is_active','modified_at']

class ListBoutiquesView(generics.ListAPIView):
    queryset = Boutique.objects.all()
    serializer_class = ListBoutiqueSerializer
    pagination_class = None
    permission_classes = [AdminAuthenticationPermission]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ['name']
    filterset_fields = ['name']
    search_fields = ['name']
    ordering_fields = ['name']

class reset_request(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = PasswordrestSerializer
    def post(self, request, *args, **kwargs):
        # return super().post(request, *args, **kwargs)
        data = request.data
        email = data['email']
        user = User.objects.get(email=email)
        if User.objects.filter(email=email).exists():
            user.otp = random.randint(1000, 9999)
            user.save()
            # send email with otp
            send_mail(
            'Réinisialiser Votre mot de passe',
            f'utilisez ce code :  {user.otp} pour réinitialiser votre mot de passe.',
            'from@example.com',
            [user.email],
            fail_silently=False,
            )
            message = {
                'detail': 'email de réinitialisation est envoyé'}
            return Response(message, status=status.HTTP_200_OK)
        else:
            message = {
                'detail': 'utilisateur avec cet email n existe pas'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)


class reset_password(generics.UpdateAPIView):
    serializer_class = PasswordResetConfirmSerializer
    queryset = User.objects.all()
    def update(self, request, *args, **kwargs):
        """reset_password with email, OTP and new password"""
        data = request.data
        user = User.objects.get(email=data['email'])
        new_password = data['new_password'] 
        new_password2 = data['new_password2'] 
        if user.is_active:
            # Check if otp is valid
            if data['otp'] == user.otp:
                if len(new_password) > 7:
                    if new_password == new_password2 :
                        # Change Password
                        user.set_password(data['new_password'])
                        user.otp = random.randint(1000, 9999)
                        user.save()
                        return Response(' vous avez réinitialisé votre mot de passe  ')
                    else :
                        return Response('les deux mot de passe ne sont pas identiques')  
                else:
                    message = {
                        'detail': 'Votre mot de passe est trop court'}
                    return Response(message, status=status.HTTP_400_BAD_REQUEST)
            else:
                message = {
                    'detail': 'OTP n est pas correcte'}
                return Response(message, status=status.HTTP_400_BAD_REQUEST)
        else:
            message = {
                'detail': 'il y a une erreur'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)

class DepartView(viewsets.ModelViewSet):
    queryset = Wilaya.objects.all()
    serializer_class = WilayaSerializer
    permission_classes = []
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ['name']
    filterset_fields = ['name']
    search_fields = ['name']
    ordering_fields = ['name']

class CompanyView(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = []
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ['name','manager']
    filterset_fields = ['name','manager']
    search_fields = ['name','manager']
    ordering_fields = ['name','manager']

class DestinationView(viewsets.ModelViewSet):
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer
    permission_classes = []
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ['depart','company','destination','desk_price','home_price','return_costs']
    filterset_fields = ['depart','company','destination','desk_price','home_price','return_costs']
    search_fields = ['depart','company','destination','desk_price','home_price','return_costs']
    ordering_fields = ['depart','company','destination','desk_price','home_price','return_costs']

class ManagerCommandsView(viewsets.ModelViewSet):
    Serializer_class = PanierSerializer
    # permission_classes = [DeliveryManagerPermission]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ['owner','detailed_place','wilaya','commune','postal_code','tel','orders','company','state','created_at']
    filterset_fields = ['owner','detailed_place','wilaya','commune','postal_code','tel','orders','company','state','created_at']
    search_fields = ['owner__id','detailed_place','wilaya','commune','postal_code','tel','orders__id','company','state','created_at']
    ordering_fields = ['owner','detailed_place','wilaya','commune','postal_code','tel','orders','company','state','created_at']
    def get_queryset(self):
        user = self.request.user
        return Panier.objects.filter(company__manager = user)

class BoutiquesOrdersStat(APIView): 
    permission_classes = [IsAuthenticated]
    def get(self , request , format = None,**kwargs):
        user = request.user
        boutique = Boutique.objects.get(owner = user)
        if kwargs.get("date", None) is not None:
            sdate = kwargs["date"]
            date = datetime.strptime(sdate,'%d-%m-%y')
        products = dict()
        products = Order.objects.filter(panier__isnull = False , created_at__gt = date ,product__boutique = boutique).values('product').annotate(total = Sum('quantity')).order_by('-total')
        data = {
            'products': products
        }
        return Response(data)

class PublicityView(viewsets.ModelViewSet):
    queryset = Publicity.objects.all()
    serializer_class = PublicitySerializer
    permission_classes = []
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ['id','title','description','image']
    filterset_fields = ['id','title','description','image']
    search_fields = ['id','title','description','image']
    ordering_fields =['id','title','description','image'] 