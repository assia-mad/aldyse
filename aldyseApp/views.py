from django.shortcuts import render
from rest_framework import viewsets
from .models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticatedOrReadOnly , IsAuthenticated
from rest_framework.filters import SearchFilter , OrderingFilter
from rest_framework.parsers import JSONParser , FormParser , MultiPartParser
from django_filters.rest_framework import DjangoFilterBackend

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
    # permission_classes = [IsAuthenticated]
    parser_classes = [FormParser, JSONParser, MultiPartParser]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ['first_name','last_name','email','wilaya','commune','tel','role','is_superuser', 'is_active']
    filterset_fields = ['first_name','last_name','email','wilaya','commune','tel','role','is_superuser', 'is_active']
    search_fields = ['first_name','last_name','email','wilaya','commune','tel','role','is_superuser', 'is_active']
    ordering_fields = ['first_name','last_name','email','wilaya','commune','tel','role','is_superuser', 'is_active']

    def get_serializer_class(self):
        serializer_class = self.serializer_class
        if self.request.method == 'PUT':
            serializer_class = UpdateUsersByAdminSerializer
        return serializer_class

class TypeView(viewsets.ModelViewSet):
    queryset = Type.objects.all()
    serializer_class = TypeSerializer
    # permission_classes = 
    filter_backends = [DjangoFilterBackend,OrderingFilter,SearchFilter]
    filter_fields = ['name']
    filterset_fields = ['name']
    search_fields = ['name']
    ordering_fields = ['name']

class CategoryView(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # permission_classes = 
    filter_backends = [DjangoFilterBackend,OrderingFilter,SearchFilter]
    filter_fields = ['name']
    filterset_fields = ['name']
    search_fields = ['name']
    ordering_fields = ['name']

class SubCategoryView(viewsets.ModelViewSet):
    queryset = SubCategory.objects.all()
    serializer_class = SubcategorySerializer
    # permission_classes = 
    filter_backends = [DjangoFilterBackend,OrderingFilter,SearchFilter]
    filter_fields = ['name','category']
    filterset_fields = ['name','category']
    search_fields = ['name','category__id']
    ordering_fields = ['name','category']

class CertificateDemandView(viewsets.ModelViewSet):
    queryset = CertificateDemand.objects.all()
    serializer_class = CertificateDemandSerializer
    # permission_classes = 
    filter_backends = [DjangoFilterBackend,OrderingFilter,SearchFilter]
    filter_fields = ['boutique','demand','is_accepted']
    filterset_fields = ['boutique','demand','is_accepted']
    search_fields = ['boutique__id','demand','is_accepted']
    ordering_fields = ['boutique','demand','is_accepted']

class CertificateDemandView(viewsets.ModelViewSet):
    serializer_class = CertificateDemandSerializer
    # permission_classes = 
 
class ListDetailView(viewsets.ReadOnlyModelViewSet):#return list of emails and ids of users
    serializer_class = ListDetailserializer
    pagination_class = None
    queryset = User.objects.all()
    filter_backends = [DjangoFilterBackend,OrderingFilter,SearchFilter]
    filter_fields = ['email']
    filterset_fields = ['email']
    search_fields = ['email']
    ordering_fields = ['email']

