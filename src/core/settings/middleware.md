

# ⚙️ Django 미들웨어 설정 README

## ✨ 개요

이 문서는 Django 프로젝트의 미들웨어 설정을 설명합니다. 미들웨어는 요청(Request)과 응답(Response) 사이에서 다양한 기능을 수행하여 웹 애플리케이션의 핵심 기능을 지원합니다.

## 🛠️ 미들웨어 설정 항목

```python
VANILA_MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
THIRD_PARTY_MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]
MIDDLEWARE = VANILA_MIDDLEWARE + THIRD_PARTY_MIDDLEWARE
```

*   **미들웨어(Middleware)**: 클라이언트로부터 요청이 들어와 뷰(View) 함수에 도달하기 전, 그리고 뷰 함수에서 응답이 생성되어 클라이언트로 보내지기 전에 실행되는 소프트웨어 구성 요소입니다. 요청 처리 파이프라인을 구성하며, 각 미들웨어는 순서대로 실행됩니다.
*   `VANILA_MIDDLEWARE`: Django 프레임워크에서 기본적으로 제공하는 미들웨어 목록입니다.
    *   `django.middleware.security.SecurityMiddleware`: 다양한 보안 관련 헤더를 추가하고 연결 보안을 강화합니다.
    *   `django.contrib.sessions.middleware.SessionMiddleware`: 세션 기능을 활성화하고 요청 객체에 세션을 연결합니다.
    *   `django.middleware.common.CommonMiddleware`: 요청 경로에 따라 URL을 정규화하고, 특정 HTTP 헤더를 처리하며, 금지된 요청을 차단하는 등의 일반적인 처리를 합니다.
    *   `django.middleware.csrf.CsrfViewMiddleware`: CSRF(Cross-Site Request Forgery) 공격으로부터 보호하기 위해 요청에 유효한 CSRF 토큰이 있는지 검사합니다. [1]
    *   `django.contrib.auth.middleware.AuthenticationMiddleware`: 요청 객체에 현재 로그인한 사용자를 나타내는 `user` 속성을 추가하여 인증 기능을 지원합니다.
    *   `django.contrib.messages.middleware.MessageMiddleware`: 일회성 알림 메시지(예: "성공적으로 저장되었습니다") 기능을 지원합니다.
    *   `django.middleware.clickjacking.XFrameOptionsMiddleware`: 클릭재킹(Clickjacking) 공격으로부터 보호하기 위해 X-Frame-Options 헤더를 추가합니다.
*   `THIRD_PARTY_MIDDLEWARE`: 프로젝트에 추가된 외부 라이브러리(서드파티 앱)에서 제공하는 미들웨어 목록입니다.
    *   `corsheaders.middleware.CorsMiddleware`: 교차 출처 리소스 공유(CORS) 정책을 처리하여, 다른 도메인의 웹 페이지에서 이 Django 서버의 리소스에 접근할 수 있도록 허용하거나 차단합니다. [2]
    *   `allauth.account.middleware.AccountMiddleware`: `django-allauth` 앱에서 계정 관리, 소셜 로그인, 회원가입, 비밀번호 재설정 등과 관련된 처리를 담당합니다.
*   `MIDDLEWARE`: Django 프로젝트에서 최종적으로 사용될 미들웨어 목록입니다. `VANILA_MIDDLEWARE`와 `THIRD_PARTY_MIDDLEWARE`를 합하여 구성합니다. 미들웨어는 이 리스트에 나열된 **순서대로** 실행되므로, 외부 라이브러리의 문서를 참고하여 올바른 위치에 배치하는 것이 중요합니다. (예: `CorsMiddleware`는 보통 다른 미들웨어보다 먼저 실행되도록 리스트의 상단에 배치됩니다.)

---
