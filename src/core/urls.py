from django.contrib import admin
from django.urls import path, include
from auth.views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [

    path('admin/', admin.site.urls),
    # path('accounts/google/login/', oauth2_login, name='google_login'),
    path('accounts/', include('allauth.urls')),
    path('callback/', google_login_callback, name='callback'),
    #############################################################
    path('api/google/validate_token/',
         validate_google_token, name='validate_token'),
    path('api/auth/user/', UserDetailView.as_view(), name='user_detail'),
    path('api/user/register/', UserCreate.as_view(), name='user_create'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),


]
