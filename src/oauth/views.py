from django.shortcuts import redirect
from django.contrib.auth.models import User
from rest_framework import generics
from .serializers import UserSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from allauth.socialaccount.models import SocialToken, SocialAccount
from django.contrib.auth.decorators import login_required
from rest_framework_simplejwt.tokens import RefreshToken


class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class UserDetailView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


@login_required
def make_token(request):
    user = request.user

    social_accounts = SocialAccount.objects.filter(user=user)
    social_account = social_accounts.first()

    if not social_account:
        return redirect('http://127.0.0.1:3000/login/callback/?error=NoSocialAccount')
    token = SocialToken.objects.filter(
        account=social_account, account__provider='google').first()

    if token:

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        return redirect(f'http://127.0.0.1:3000/login/callback/?access_token={access_token}&refresh_token={refresh_token}')
    else:
        return redirect(f'http://127.0.0.1:3000/login/callback/?error=NoGoogleTokenFound')
