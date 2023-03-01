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
from django.db.models import Sum ,Count
from itertools import chain
from django.core.cache import cache


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
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ['boutique','name','price','discount_percentage','gender','product_type','sub_category','available_colors','size_type','available_sizes','published_by','sub_category__category','created_at']
    filterset_fields = ['boutique','name','price','discount_percentage','gender','product_type','sub_category','available_colors','size_type','available_sizes','published_by','sub_category__category','created_at']
    search_fields = ['boutique__id','name','price','discount_percentage','gender','product_type__id','sub_category__id','available_colors__id','size_type__id','available_sizes__id','published_by','sub_category__category__id','created_at']
    ordering_fields = ['boutique','name','price','discount_percentage','gender','product_type','sub_category','available_colors','size_type','available_sizes','published_by''sub_category__category','created_at']
    def get_object(self):
        product = super().get_object()
        user = self.request.user
        cached_data = cache.get(user.pk)
        if cached_data is None:
            cached_data = [product.sub_category]
        else :
            if not (product.sub_category in cached_data):
                cached_data.append(product.sub_category)
        cache.set(user.pk , cached_data , 3600*60)
        print("we cached .......",cache.get(user.pk))
        return product

    def destroy(self, request, *args, **kwargs):
        product = self.get_object()
        print(product)
        orders = Order.objects.filter(product=product)
        if orders is not None :
            for order in orders:
                title = "produit supprimé"
                description = "Le produit"+product.name+"a été supprimé"
                Notification.objects.create(user=order.owner,title=title,description=description)
                panier_id = order.panier.id
                if panier_id is not None :
                    panier = Panier.objects.filter(pk=panier_id).first()
                    print("before deleting",panier.total_price)
                    #do price changes for the panier
                    panier.total_price -= order.price
                    print("after deleting",panier.total_price)
                    depart = order.product.boutique.wilaya
                    wilaya_destination = panier.wilaya
                    home_delivery = panier.home_delivery
                    company = panier.company
                    destination = Destination.objects.filter(company = company , destination= wilaya_destination , depart = depart).first()
                    print("the destination",destination)
                    print("delivery price",panier.delivery_price)
                    if home_delivery:
                        price = destination.home_price
                    else:
                        price = destination.desk_price
                    panier.delivery_price -= price
                    print("delivery price",panier.delivery_price)
                    panier.save()
                    if panier.total_price == 0.0 :
                        panier.delete()
                order.delete()
        self.perform_destroy(product)
        return Response(status=status.HTTP_204_NO_CONTENT)

class OrderView(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    pagination_class = None
    # permission_classes = [IsAuthenticated , AdminOrownerPermission]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ['owner','panier','product','color','size','quantity','price','created_at']
    filterset_fields = ['owner','panier','product','color','size','quantity','price','created_at']
    search_fields = ['owner__id','panier__id','product__id','color','size','quantity','price','created_at']
    ordering_fields = ['owner','panier','product','color','size','quantity','price','created_at']

    def get_queryset(self):
        if self.request.query_params.get('panier_null', "false") == "true":
            return Order.objects.filter( panier__isnull = True)
        return Order.objects.all()

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

class ListBoutiquesView(viewsets.ModelViewSet):
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
    serializer_class = PanierSerializer
    permission_classes = [DeliveryManagerPermission]
    pagination_class = CustomPagination_4
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
        if kwargs.get("state", None) is not None:
            k_state= kwargs["state"]
        products = dict()
        products = Order.objects.filter(panier__isnull = False , created_at__gt = date ,product__boutique = boutique,panier__state=k_state).values('product').annotate(total = Sum('quantity')).order_by('-total')
        data = {
            'products': products
        }
        return Response(data)

class PublicityView(viewsets.ModelViewSet):
    queryset = Publicity.objects.all()
    serializer_class = PublicitySerializer
    permission_classes = []
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ['title','description','created_at']
    filterset_fields = ['title','description','created_at']
    search_fields = ['title','description','created_at']
    ordering_fields =['title','description','created_at']

class SignalView(viewsets.ModelViewSet):
    queryset = Signal.objects.all()
    serializer_class = SignalSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ['user','description','created_at']
    filterset_fields = ['user','description','created_at']
    search_fields = ['user__id','description','created_at']
    ordering_fields =['user','description','created_at']

class DeliveryPrice(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        departs = []
        price = 0
        orders_ids = kwargs.get("orders", None)
        orders_values = orders_ids.split(',')
        if orders_values is not None : 
            orders = Order.objects.filter(pk__in = orders_values)
            for order in orders :
                depart = order.product.boutique.wilaya
                if (depart.id)not in departs : 
                    departs.append(depart.id)
        wilaya_destination = kwargs.get("wilaya_dest", None)
        company = kwargs.get("company",None)
        home_delivery = kwargs.get("home_delivery",None)
        if (company is not None) and (wilaya_destination is not None):
            destinations = Destination.objects.filter(company = company , destination= wilaya_destination , depart__in = departs).all()
            if destinations is not None :
                if home_delivery == "True":
                    for destination in destinations:
                        print("home dest",destination)
                        print(" home her price", destination.home_price)
                        price += destination.home_price
                else :
                    for destination in destinations:
                        print("desk dest",destination)
                        print("desk her price", destination.desk_price)
                        price += destination.desk_price
            else :
                return Response({"erreur":"la destination est érroné"})
        data = {
            'prix_livraison': price,
        }
        return Response(data)

class SuggestedProductsView(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ['boutique','name','price','discount_percentage','gender','product_type','sub_category','available_colors','size_type','available_sizes','published_by','sub_category__category','created_at']
    filterset_fields = ['boutique','name','price','discount_percentage','gender','product_type','sub_category','available_colors','size_type','available_sizes','published_by','sub_category__category','created_at']
    search_fields = ['boutique__id','name','price','discount_percentage','gender','product_type__id','sub_category__id','available_colors__id','size_type__id','available_sizes__id','published_by','sub_category__category__id','created_at']
    ordering_fields = ['boutique','name','price','discount_percentage','gender','product_type','sub_category','available_colors','size_type','available_sizes','published_by''sub_category__category','created_at']
    def get_queryset(self):
        orders_list = Order.objects.order_by('created_at').filter(owner = self.request.user)[:15]
        favorites = FavoriteList.objects.get(owner = self.request.user).products.all()
        visited_sub_categories = cache.get(self.request.user.pk)
        print("the visited",visited_sub_categories)
        print("the fav",favorites)
        print("orders",orders_list)
        if all(v is None for v in [orders_list, favorites, visited_sub_categories]):
            print("hiiiiiiiiiiiiiiiiiiiiiii")
            return Product.objects.all().order_by('?')
        else :
            suggestes_sub_categories = [] #suggest based on them
            purchasted_products = [] #to eleminate them from suggestions
            suggested_types = [] # suggest products by tags too
            if visited_sub_categories is not None :
                suggestes_sub_categories.extend(visited_sub_categories)
            if orders_list is not None :
                for order in orders_list:
                    purchasted_products.append(order.product.pk)
                    sub_category = order.product.sub_category
                    type = order.product.product_type
                    if not ( sub_category in suggestes_sub_categories) :
                        suggestes_sub_categories.append(sub_category)
                    if not ( type  in suggested_types):
                        suggested_types.append(type)
            if favorites is not None :
                for product in favorites.all() :
                    purchasted_products.append(product.pk)
                    if not (product.sub_category in suggestes_sub_categories):
                        suggestes_sub_categories.append(product.sub_category)
                    if not ( product.product_type  in suggested_types):
                        suggested_types.append(product.product_type )
            print("the suggested sub categories....",suggestes_sub_categories)
            print("the suggested types.......",suggested_types)
            suggested_products1 = Product.objects.filter(sub_category__in = suggestes_sub_categories,product_type__in = suggested_types).exclude(pk__in = purchasted_products).order_by('?')[:30]
            random_products = Product.objects.exclude(pk__in=suggested_products1).order_by('?')[:25]
            result_queryset = random_products |suggested_products1  
        return result_queryset
       

class BoutiqueOrdersView(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ['owner','panier','product','color','size','quantity','created_at','panier__state']
    filterset_fields = ['owner','panier','product','color','size','quantity','created_at','panier__state']
    search_fields = ['owner__id','panier__id','product__id','color','size','quantity','created_at']
    ordering_fields = ['owner','panier','product','color','size','quantity','state','created_at']
    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(product__boutique__owner = user)


class DeliveryStats(generics.ListAPIView):
    serializer_class = PanierSerializer
    permission_classes = [DeliveryManagerPermission]
    pagination_class = None
    def get(self, request, *args, **kwargs):
        user = request.user
        total_orders = 0
        orders_price = 0
        delivery_price = 0
        if kwargs.get("date", None) is not None:
            sdate = kwargs["date"]
            date = datetime.strptime(sdate,'%d-%m-%y')
        if kwargs.get("state", None) is not None:
            k_state= kwargs["state"]
        paniers = Panier.objects.filter(company__manager = user , created_at__gte = date,state=k_state).all()
        for panier in paniers:
            delivery_price += panier.delivery_price
            orders_price += panier.total_price
            total_orders+= panier.orders.count()
        data = {
            'total_orders': total_orders,
            'orders_price': orders_price,
            'delivery_price': delivery_price,
        }
        return Response(data)
    
class BoutiquesStats(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [AdminAuthenticationPermission]
    pagination_class = None
    def get(self, request, *args, **kwargs):
        if kwargs.get("date", None) is not None:
            sdate = kwargs["date"]
            date = datetime.strptime(sdate,'%d-%m-%y')
        if kwargs.get("state", None) is not None:
            k_state= kwargs["state"]
        boutiques = Order.objects.filter(created_at__gte = date , panier__isnull = False,panier__state=k_state).values('product__boutique').annotate(total = Sum('quantity')).order_by('-total')
        data = {'boutiques' : boutiques}
        return Response(data)

class SubCategoriesStats(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [AdminAuthenticationPermission]
    pagination_class = None
    def get(self, request, *args, **kwargs):
        if kwargs.get("date", None) is not None:
            sdate = kwargs["date"]
            date = datetime.strptime(sdate,'%d-%m-%y')
        if kwargs.get("state", None) is not None:
            k_state= kwargs["state"]
        sub_categories = Order.objects.filter(created_at__gte = date , panier__isnull = False,panier__state=k_state).values('product__sub_category').annotate(total = Sum('quantity')).order_by('-total')
        data = {'sub_categories' : sub_categories}
        return Response(data)

class DeliveryCompaniesStats(generics.ListAPIView):
    serializer_class = PanierSerializer
    permission_classes = [AdminAuthenticationPermission]
    pagination_class = None
    def get(self, request, *args, **kwargs):
        if kwargs.get("date", None) is not None:
            sdate = kwargs["date"]
            date = datetime.strptime(sdate,'%d-%m-%y')
        if kwargs.get("state", None) is not None:
            k_state= kwargs["state"]
        companies = Panier.objects.filter(created_at__gte = date , state = k_state).values('company').annotate(total = Count('orders')).order_by('-total')
        data = {'companies' : companies}
        return Response(data)

class TypeStats(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    pagination_class = None
    def get(self, request, *args, **kwargs):
        if kwargs.get("date", None) is not None:
            sdate = kwargs["date"]
            date = datetime.strptime(sdate,'%d-%m-%y')
        if kwargs.get("state", None) is not None:
            k_state= kwargs["state"]
        types = Order.objects.filter(created_at__gte = date , panier__isnull = False,panier__state=k_state).values("product__product_type").annotate(total = Sum('quantity')).order_by('-total')
        data = {'types':types}
        return Response(data)


class WialayasStats(generics.ListAPIView):
    serializer_class = PanierSerializer
    permission_classes = [AdminAuthenticationPermission]
    pagination_class = None
    def get(self, request, *args, **kwargs):
        if kwargs.get("date", None) is not None:
            sdate = kwargs["date"]
            date = datetime.strptime(sdate,'%d-%m-%y')
        if kwargs.get("state", None) is not None:
            k_state= kwargs["state"]
        wilayas = Panier.objects.filter(created_at__gte = date, state=k_state).values('wilaya').annotate(total = Count('orders')).order_by('-total')
        data = {'wilayas' : wilayas}
        return Response(data)

class JustificationView(viewsets.ModelViewSet):
    queryset = Justification.objects.all()
    serializer_class = JustificationSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ['user','panier','description','created_at']
    filterset_fields = ['user','panier','description','created_at']
    search_fields = ['user__id','panier__id','description','created_at']
    ordering_fields =['user','panier','description','created_at']

class NotificationView(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ['user','title','description','created_at']
    filterset_fields = ['user','title','description','created_at']
    search_fields = ['user__id','title','description','created_at']
    ordering_fields =['user','title','description','created_at']