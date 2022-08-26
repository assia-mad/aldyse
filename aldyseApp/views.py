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

# manage users by Admin
class ManageUsersView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = ManageusersSerializer
    permission_classes = [IsAuthenticated]
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
