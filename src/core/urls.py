from django.contrib import admin
from django.urls import path, include
from auth.views import *
from board.views import CounterAPIView  # 위에서 만든 View 클래스 가져오기
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [

    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('callback/', make_token, name='callback'),
    path('api/auth/user/', UserDetailView.as_view(), name='user_detail'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]+[path('api/counter/', CounterAPIView.as_view(), name='counter_api'),]
