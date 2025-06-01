from django.shortcuts import redirect
from django.contrib.auth.models import User
from rest_framework import generics
from .serializers import UserSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from allauth.socialaccount.models import SocialToken, SocialAccount
from django.contrib.auth.decorators import login_required
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
from utils.env import ENV
import json


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
def google_login_callback(request):
    user = request.user

    social_accounts = SocialAccount.objects.filter(user=user)
    print("Social Account for user:", social_accounts)

    social_account = social_accounts.first()

    if not social_account:
        print("No social account for user:", user)
        return redirect('http://127.0.0.1:3000/login/callback/?error=NoSocialAccount')

    token = SocialToken.objects.filter(
        account=social_account, account__provider='google').first()

    if token:
        print('Google token found:', token.token)
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        return redirect(f'http://127.0.0.1:3000/login/callback/?access_token={access_token}')
    else:
        print('No Google token found for user', user)
        return redirect(f'http://127.0.0.1:3000/login/callback/?error=NoGoogleToken')


@csrf_exempt
def validate_google_token(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            google_id_token = data.get('access_token')
            print('|', google_id_token, '|')

            if not google_id_token:
                return JsonResponse({'detail': 'ID Token is missing.'}, status=400)

            google_tokeninfo_url = f"https://oauth2.googleapis.com/tokeninfo?id_token={google_id_token}"

            try:
                response = requests.get(google_tokeninfo_url)
                response_data = response.json()

                if response.status_code == 200:
                    if response_data.get("aud") != ENV["GOOGLE_CLIENT_ID"]:
                        return JsonResponse({'valid': False, 'detail': 'Invalid audience.'}, status=401)
                    return JsonResponse({'valid': True, 'user_info': response_data})
                else:
                    return JsonResponse({'valid': False, 'detail': response_data.get('error_description', 'Invalid ID token')}, status=401)

            except requests.exceptions.RequestException as e:
                print(f"Error during Google token validation request: {e}")
                return JsonResponse({'detail': 'Error validating token with Google.'}, status=500)

        except json.JSONDecodeError:
            return JsonResponse({'detail': 'Invalid JSON.'}, status=400)
    return JsonResponse({'detail': 'Method not allowed.'}, status=405)
