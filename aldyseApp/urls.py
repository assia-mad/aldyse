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


urlpatterns = [
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('account-confirm-email/<str:key>/', ConfirmEmailView.as_view()),
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('accounts/', include('allauth.urls'), name='socialaccount_signup'),
    path('verify-email/', VerifyEmailView.as_view(), name='rest_verify_email'),
    path('account-confirm-email/', VerifyEmailView.as_view(), name='account_email_verification_sent'),
    re_path(r'^account-confirm-email/(?P<key>[-:\w]+)/$',VerifyEmailView.as_view(), name='account_confirm_email'),
    path('password-reset/', PasswordResetView.as_view()),
    path('password-change/',PasswordChangeView.as_view()),
    path('user/', UserDetailsView.as_view()),
    re_path('^pro/(?P<name>.+)/$',ProductCategoryList.as_view()),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

]
urlpatterns += router.urls