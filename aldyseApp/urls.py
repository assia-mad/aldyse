from django.urls import path , include , re_path
from dj_rest_auth.registration.views import RegisterView , ConfirmEmailView , VerifyEmailView
from dj_rest_auth.views import UserDetailsView, LoginView, LogoutView , PasswordResetView , PasswordResetConfirmView , PasswordChangeView
from rest_framework import routers
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from aldyseApp.views import *

schema_view = get_schema_view(

   openapi.Info(

      title="Aldyse API",
      default_version='v1',
      description="Aldyse is an e-commerce application ",
      contact=openapi.Contact(email="soon@gmail.com"),
      license=openapi.License(name="BSD License"),

   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

router = routers.DefaultRouter()
router.register('manage_users', ManageUsersView , basename='manage_users')
router.register('boutiques', BoutiqueView , basename='boutiques')
router.register('types', TypeView , basename='types')
router.register('categories', CategoryView , basename='categories')
router.register('sub_categories', SubCategoryView, basename='sub_categories')
router.register('certificate_demands',CertificateDemandView , basename='certificate_demands')
router.register('users_details',ListDetailView , basename='users_details')
router.register('colors', ColorView , basename='product_colors')
router.register('sizes', SizeView, basename='product_sizes')
router.register('size_types', SizeTypeView, basename='size_types')
router.register('images',ProductImageView , basename='images')
router.register('products', ProductView , basename='products')
router.register('orders',OrderView , basename='orders')
router.register('paniers',PanierView , basename='paniers')
router.register('non_validated_boutiques',NonValidatedBoutiqueView , basename='non_validated_boutique')
router.register('favorites', FavoriteListView, basename='favorites')
router.register('happy_hours',HappyHourView, basename='happy_hours')
router.register('companies',CompanyView, basename='companies')
router.register('wilayas',DepartView, basename='wilayas')
router.register('destinations',DestinationView, basename='destinations')
router.register('manager_commands', ManagerCommandsView , basename='manager_commands')
router.register('boutique_orders', BoutiqueOrdersView , basename = 'boutique_orders')


urlpatterns = [
    path('password-reset-confirm/', reset_password.as_view(), name='password_reset_confirm'),
    path('account-confirm-email/<str:key>/', ConfirmEmailView.as_view()),
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('accounts/', include('allauth.urls'), name='socialaccount_signup'),
    path('verify-email/', VerifyEmailView.as_view(), name='rest_verify_email'),
    path('account-confirm-email/', VerifyEmailView.as_view(), name='account_email_verification_sent'),
    re_path(r'^account-confirm-email/(?P<key>[-:\w]+)/$',VerifyEmailView.as_view(), name='account_confirm_email'),
    path('password-reset/', reset_request.as_view()),
    path('password-change/',PasswordChangeView.as_view()),
    path('user/', UserDetailsView.as_view()),
    path('list_boutiques/',ListBoutiquesView.as_view()),
    path('stats_boutique/<str:date>/', BoutiquesOrdersStat.as_view()),
    path('delivery_price/<str:orders>/<int:wilaya_dest>/<int:company>/<str:home_delivery>/',DeliveryPrice.as_view()),
    path('suggestions/', SuggestedProductsView.as_view() , name = 'suggestions'),
    path('stats_delivery/<str:date>/', DeliveryStats.as_view(), name ='stats_delivery'),
    path('stats_boutiques/<str:date>/', BoutiquesStats.as_view(), name ='stats_boutiques'),
    path('stats_subcategories/<str:date>/', SubCategoriesStats.as_view(), name ='stats_subcategories'),
    path('stats_companies/<str:date>/', DeliveryCompaniesStats.as_view(), name ='stats_companies'),
    path('stats_wilayas/<str:date>/', WialayasStats.as_view(), name ='stats_wilayas'),
    re_path('^pro/(?P<name>.+)/$',ProductCategoryList.as_view()),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

]
urlpatterns += router.urls