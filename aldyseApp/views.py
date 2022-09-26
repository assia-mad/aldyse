from django.shortcuts import render
from rest_framework import viewsets , generics
from .models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticatedOrReadOnly , IsAuthenticated
from rest_framework.filters import SearchFilter , OrderingFilter
from rest_framework.parsers import JSONParser , FormParser , MultiPartParser
from django_filters.rest_framework import DjangoFilterBackend
from .pagination import *
from .permissions import *

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
    filter_fields = ['owner','detailed_place','wilaya','commune','postal_code','tel']
    filterset_fields = ['owner','detailed_place','wilaya','commune','postal_code','tel']
    search_fields = ['owner__id','detailed_place','wilaya','commune','postal_code','tel']
    ordering_fields = ['owner','detailed_place','wilaya','commune','postal_code','tel']

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

        
    



    

