

# 🚀 Django 인증 및 소셜 로그인 (Google) 설정 README

## ✨ 개요

이 문서는 Django 프로젝트에서 Django REST Framework를 사용하여 인증(JWT 포함)과 `django-allauth`를 활용한 Google 소셜 로그인을 설정하는 내용을 담고 있습니다. 주요 설정 항목들을 정리하여 개발 및 유지보수에 도움이 되도록 합니다.

## 🛠️ 주요 설정 항목

### 1. 일반 설정

```python
SOCIALACCOUNT_LOGIN_ON_GET = True
LOGIN_REDIRECT_URL = '/callback/'
SOCIALACCOUNT_STORE_TOKENS = True
```

*   `SOCIALACCOUNT_LOGIN_ON_GET`: GET 요청으로도 소셜 로그인 시작 페이지에 접근 가능하게 합니다. 보안상 `False`로 설정하는 것이 권장될 수 있습니다.
*   `LOGIN_REDIRECT_URL`: 로그인이 성공적으로 완료된 후 리다이렉트될 URL입니다. 여기서는 프론트엔드 애플리케이션 주소로 설정되어 있습니다.
*   `SOCIALACCOUNT_STORE_TOKENS`: 소셜 프로바이더로부터 받은 토큰(Access Token, Refresh Token 등)을 저장할지 여부를 설정합니다. `True`로 설정하면 유저의 소셜 계정 정보를 활용할 수 있습니다.

### 2. 인증 백엔드 설정

```python
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]
```

*   `django.contrib.auth.backends.ModelBackend`: Django의 기본 인증 백엔드로, 사용자 모델을 기반으로 인증합니다.
*   `allauth.account.auth_backends.AuthenticationBackend`: `django-allauth`의 인증 백엔드로, 소셜 로그인 등을 처리합니다.

### 3. Django REST Framework 설정

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    )
}
```

*   `DEFAULT_AUTHENTICATION_CLASSES`: API 요청에 사용될 기본 인증 클래스를 정의합니다. `JWTAuthentication`은 Simple JWT를, `SessionAuthentication`은 Django 세션을 이용한 인증을 처리합니다.
*   `DEFAULT_PERMISSION_CLASSES`: API 요청에 적용될 기본 권한 클래스를 정의합니다. `IsAuthenticated`는 인증된 사용자만 접근을 허용합니다.

### 4. Django Simple JWT 설정

```python
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_ENABLED': True,
}
```

*   `ACCESS_TOKEN_LIFETIME`: 액세스 토큰의 유효 기간을 설정합니다 (여기서는 5분).
*   `REFRESH_TOKEN_LIFETIME`: 리프레시 토큰의 유효 기간을 설정합니다 (여기서는 1일).
*   `ROTATE_REFRESH_TOKENS`: 리프레시 토큰 사용 시 새로운 리프레시 토큰을 발급받을지 여부입니다. `False`로 설정되어 있습니다.
*   `BLACKLIST_ENABLED`: 사용된 토큰을 블랙리스트 처리할지 여부입니다. `False`로 설정되어 있습니다.

### 5. 소셜 계정 프로바이더 설정 (Google)

```python
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        },
        'OAUTH_PKCE_ENABLED': True,
        'FETCH_USERINFO': True,
    }
}
```

*   `'google'`: Google 소셜 로그인 설정을 의미합니다.
*   `SCOPE`: Google API로부터 요청할 사용자 정보 범위를 지정합니다 (`profile`, `email`).
*   `AUTH_PARAMS`: 인증 요청 시 추가 파라미터를 설정합니다 (`access_type='online'`은 오프라인 접근 권한을 요청하지 않음을 의미합니다).
*   `OAUTH_PKCE_ENABLED`: OAuth 2.0 PKCE(Proof Key for Code Exchange) 확장을 사용할지 여부입니다. 보안 강화를 위해 `True`로 설정하는 것이 권장됩니다.
*   `FETCH_USERINFO`: 인증 후 Google로부터 사용자 정보를 추가로 가져올지 여부입니다. `True`로 설정되어 있습니다.




# SITE ID
* 에러나면 2~5 값 중에 하나 넣을것

# Change social application
* Provider: Google
* Name: Google
* Client id: ~
* Secret key: ~


# 승인된 JavaScript 원본
* http://127.0.0.1:3000
* http://localhost:3000

# 승인된 리디렉션 URI
* http://localhost:8000/accounts/google/login/callback/
* http://127.0.0.1:8000/accounts/google/login/callback/