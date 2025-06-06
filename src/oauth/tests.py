import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from allauth.socialaccount.models import SocialAccount, SocialToken
from django.conf import settings
from urllib.parse import urlparse, parse_qs  # 리다이렉트 URL 분석하려고 필요한 친구들!

# Django의 기본 User 모델 가져오기
User = get_user_model()

# 테스트용 사용자를 만드는 픽스처


@pytest.fixture
def test_user(db):  # db 픽스처는 pytest-django가 제공해줘서 테스트용 DB를 쓸 수 있게 해줘!
    """테스트용 사용자 생성."""
    # create_user는 비밀번호 해싱까지 알아서 해줘서 편하답니다!
    return User.objects.create_user(username='testuser', password='password123')

# 테스트용 사용자에 연결된 Google 소셜 계정을 만드는 픽스처


@pytest.fixture
def google_social_account(db, test_user):
    """테스트 사용자를 위한 Google 소셜 계정 생성."""
    return SocialAccount.objects.create(
        user=test_user,       # 위에서 만든 테스트 사용자에게 연결!
        provider='google',    # Google 계정이라고 알려주기
        uid='1234567890_dummy_uid',  # 가짜 고유 ID
        extra_data={}         # 필요한 정보 있으면 여기 추가!
    )

# Google 소셜 계정에 연결된 SocialToken을 만드는 픽스처


@pytest.fixture
def google_social_token(db, google_social_account):
    """Google 소셜 계정을 위한 SocialToken 생성."""
    # make_token 뷰는 이 SocialToken이 '있는지' 확인하는 거라 실제 토큰 값은 중요하지 않아!
    # JWT 토큰은 뷰 안에서 새로 만드는 거거든! 😉
    return SocialToken.objects.create(
        account=google_social_account,  # 위에서 만든 Google 소셜 계정에 연결!
        token='dummy_social_access_token',  # 가짜 소셜 액세스 토큰
        token_secret='',  # Google OAuth2에서는 보통 안 써요
        expires_at=None  # 만료 기한 없거나 미래 날짜로 설정!
    )

# make_token 뷰 테스트 (성공 케이스: JWT 토큰 리다이렉트 확인)


def test_make_token_redirects_with_jwt(client, test_user, google_social_account, google_social_token):
    """
    /callback/ 뷰가 로그인된 사용자에게 JWT 토큰을 포함하여 리다이렉트하는지 테스트.
    사용자는 Google 소셜 계정과 토큰을 가지고 있는 상태여야 해!
    """
    # 테스트 사용자로 로그인 시키기! client.force_login() 사용!
    client.force_login(test_user)

    # 'callback' URL 이름으로 URL 가져오기
    callback_url = reverse('callback')

    # /callback/ URL로 GET 요청 보내기!
    response = client.get(callback_url)

    # 응답 상태 코드가 리다이렉트 (302)인지 확인!
    assert response.status_code == 302

    # 리다이렉트되는 URL 가져오기 (응답 헤더의 'Location'에 있어!)
    redirect_url = response.url

    # 리다이렉트 URL이 우리가 예상하는 프론트엔드 URL로 시작하는지 확인!
    expected_base_url = 'http://127.0.0.1:3000/login/callback/'
    assert redirect_url.startswith(expected_base_url)

    # 리다이렉트 URL에서 쿼리 파라미터(access_token, refresh_token)가 잘 넘어왔는지 확인하기!
    parsed_url = urlparse(redirect_url)  # URL을 구성 요소로 분해!
    query_params = parse_qs(parsed_url.query)  # 쿼리 문자열을 딕셔너리로 파싱!

    # 'access_token'이랑 'refresh_token' 키가 쿼리 파라미터에 있는지 확인!
    assert 'access_token' in query_params
    assert 'refresh_token' in query_params

    # (선택 사항) 토큰 값이 비어있지 않은지 확인!
    assert query_params['access_token'][0] != ''
    assert query_params['refresh_token'][0] != ''

# --- 에러 케이스 테스트도 해볼까요? ---

# make_token 뷰 테스트 (에러 케이스 1: 로그인했지만 소셜 계정이 없을 때)


def test_make_token_no_social_account(client, test_user):
    """
    /callback/ 뷰가 로그인된 사용자에게 소셜 계정이 없을 때
    'NoSocialAccount' 에러와 함께 리다이렉트하는지 테스트.
    """
    # 테스트 사용자로 로그인!
    client.force_login(test_user)
    callback_url = reverse('callback')

    # GET 요청 보내기
    response = client.get(callback_url)

    # 응답 상태 코드가 리다이렉트 (302)인지 확인!
    assert response.status_code == 302

    # 리다이렉트 URL이 'NoSocialAccount' 에러를 포함하는지 확인!
    redirect_url = response.url
    expected_error_url = 'http://127.0.0.1:3000/login/callback/?error=NoSocialAccount'
    assert redirect_url == expected_error_url

# make_token 뷰 테스트 (에러 케이스 2: 로그인했고 소셜 계정은 있지만 Google 토큰이 없을 때)


def test_make_token_no_google_token(client, test_user, google_social_account):
    """
    /callback/ 뷰가 로그인된 사용자에게 Google 토큰이 없을 때
    'NoGoogleTokenFound' 에러와 함께 리다이렉트하는지 테스트.
    (google_social_account 픽스처는 Google 계정을 만들어주지만, google_social_token 픽스처는 사용 안 해서 토큰이 없는 상황 시뮬레이션!)
    """
    # 테스트 사용자로 로그인!
    client.force_login(test_user)
    callback_url = reverse('callback')

    # GET 요청 보내기
    response = client.get(callback_url)

    # 응답 상태 코드가 리다이렉트 (302)인지 확인!
    assert response.status_code == 302

    # 리다이렉트 URL이 'NoGoogleTokenFound' 에러를 포함하는지 확인!
    redirect_url = response.url
    expected_error_url = 'http://127.0.0.1:3000/login/callback/?error=NoGoogleTokenFound'
    assert redirect_url == expected_error_url

# make_token 뷰 테스트 (에러 케이스 3: 로그인 안 한 사용자)
# @login_required 데코레이터가 붙어 있어서 로그인 안 했으면 로그인 페이지로 리다이렉트 시켜요!


def test_make_token_not_authenticated(client):
    """
    /callback/ 뷰가 로그인 안 한 사용자에게 로그인 페이지로 리다이렉트하는지 테스트.
    """
    callback_url = reverse('callback')

    # 로그인 안 한 상태로 GET 요청 보내기
    response = client.get(callback_url)

    # 응답 상태 코드가 리다이렉트 (302)인지 확인!
    assert response.status_code == 302

    # 리다이렉트 URL이 allauth의 로그인 URL인지 확인!
    # 보통 settings.LOGIN_URL에 설정되어 있어요. allauth 기본값은 '/accounts/login/'
    # pytest-django는 settings를 로드해주니 settings.LOGIN_URL을 바로 쓸 수 있답니다!
    expected_login_redirect_base = settings.LOGIN_URL  # '/accounts/login/' 일 확률이 높아요!

    # 리다이렉트 URL 파싱해서 경로와 쿼리 파라미터 확인
    parsed_redirect_url = urlparse(response.url)
    parsed_expected_url = urlparse(expected_login_redirect_base)

    # 경로가 로그인 URL 경로와 일치하는지 확인
    assert parsed_redirect_url.path == parsed_expected_url.path

    # 쿼리 파라미터에 'next'가 있는지 (원래 가려던 callback URL이 잘 따라가는지) 확인!
    query_params = parse_qs(parsed_redirect_url.query)
    assert 'next' in query_params
    # 'next' 파라미터 값이 원래 callback URL과 일치하는지 확인
    assert query_params['next'][0] == callback_url

# UserDetailView 테스트 (로그인한 사용자만 접근 가능)


def test_user_detail_authenticated(client, test_user):
    """
    /api/auth/user/ 뷰에 로그인한 사용자가 접근할 수 있는지 테스트.
    """

    client.force_login(test_user)

    user_detail_url = reverse('user_detail')

    response = client.get(user_detail_url)

    assert response.status_code == 200

    assert response.json()['username'] == 'testuser'


def test_user_detail_unauthenticated(client):
    """
    /api/auth/user/ 뷰에 로그인 안 한 사용자가 접근할 수 없는지 테스트.
    (JWT 인증이 필요하므로 401 Unauthorized 또는 403 Forbidden 예상)
    """
    user_detail_url = reverse('user_detail')

    response = client.get(user_detail_url)

    assert response.status_code in [401, 403]
