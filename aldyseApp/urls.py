from django.urls import path , include , re_path
from dj_rest_auth.registration.views import RegisterView , ConfirmEmailView , VerifyEmailView
from dj_rest_auth.views import UserDetailsView, LoginView, LogoutView , PasswordResetView , PasswordResetConfirmView , PasswordChangeView
from rest_framework import routers

from aldyseApp.views import BoutiqueView

router = routers.DefaultRouter()
router.register('boutiques', BoutiqueView , basename='boutiques')


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

]
urlpatterns += router.urls