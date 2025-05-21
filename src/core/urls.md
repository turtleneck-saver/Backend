### `urls.py` 설명

이 파일은 우리 프로젝트의 **API 주소(URL)**와 해당 주소로 요청이 왔을 때 **어떤 기능을 실행할지** 연결해 주는 파일임. 쉽게 말해, 인터넷 주소창에 뭘 입력했을 때 서버의 어느 부분(View)이 응답할지를 정해 놓은 지도 같은 거임.

```python
from django.contrib import admin # Django 관리자 페이지 관련 기능 가져옴
from django.urls import path, include # URL 패턴 정의하는 기본 기능 가져옴
from auth.views import * # home 앱의 views.py 파일에 있는 모든 함수/클래스 가져옴 (사용자 생성, 구글 로그인 콜백 등)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView # JWT 인증 관련 뷰 가져옴 (토큰 발급, 토큰 갱신)


urlpatterns = [
    # 여기에 우리 서비스의 다양한 주소(URL)와 연결된 기능(View)들을 정의함

    path('admin/', admin.site.urls),
    # /admin/ 주소로 오면 Django 기본 관리자 페이지 보여줌. 데이터 관리할 때 씀.

    path('accounts/', include('allauth.urls')),
    # /accounts/ 로 시작하는 주소들은 'allauth'라는 외부 앱에서 처리하게 연결.
    # 'allauth'는 소셜 로그인(구글, 카카오 등)이나 일반 회원가입/로그인 같은 기능 쉽게 만들게 해주는 앱임.

    path('callback/', google_login_callback, name='callback'),
    # /callback/ 주소로 오면 home 앱의 google_login_callback 함수 실행.
    # 보통 구글 로그인 성공 후 구글에서 우리 서비스로 다시 돌아올 때 사용하는 주소임.

    path('api/user/register/', UserCreate.as_view(), name='user_create'),
    # /api/user/register/ 주소로 POST 요청이 오면 home 앱의 UserCreate 뷰 실행.
    # 여기서 새로운 사용자를 만듦 (회원가입 API).

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # /api/token/ 주소로 POST 요청이 오면 JWT 인증에서 쓰는 TokenObtainPairView 실행.
    # 사용자 이름, 비밀번호로 로그인해서 접근 토큰(Access Token)과 갱신 토큰(Refresh Token)을 처음 받을 때 씀.

    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # /api/token/refresh/ 주소로 POST 요청이 오면 JWT 인증에서 쓰는 TokenRefreshView 실행.
    # 기존 갱신 토큰으로 새 접근 토큰을 다시 받을 때 씀. (접근 토큰 만료 시)

    path('api-auth/', include('rest_framework.urls')),
    # /api-auth/ 로 시작하는 주소들은 DRF 기본 인증 뷰에서 처리.
    # 이건 주로 DRF의 웹 브라우저 API 화면에서 로그인/로그아웃 버튼 보여줄 때 사용함. 필수는 아님.

    path('api/auth/user/', UserDetailView.as_view(), name='user_detail'),
    # /api/auth/user/ 주소로 요청이 오면 home 앱의 UserDetailView 실행.
    # 현재 로그인된 사용자의 정보를 조회하거나(GET) 수정/삭제(PUT/DELETE)할 때 쓰는 주소일 거임.

    path('api/google/validate_token/',
         validate_google_token, name='validate_token'),
    # /api/google/validate_token/ 주소로 오면 home 앱의 validate_google_token 함수 실행.
    # 구글 로그인으로 받은 토큰이 유효한지 백엔드에서 검증할 때 사용하는 주소로 보임.
]
```

**정리:**

이 `urls.py` 파일은 관리자 페이지, 소셜 로그인(`allauth`), 일반 회원가입/로그인(`UserCreate`, `TokenObtainPairView`, `TokenRefreshView`, `UserDetailView`), 그리고 구글 토큰 검증(`validate_google_token`) 등 사용자 인증 및 관리에 필요한 주요 API 주소들을 설정해 놓은 곳임. 클라이언트(리액트 등)는 여기에 정의된 주소로 요청을 보내서 필요한 기능을 사용함.

