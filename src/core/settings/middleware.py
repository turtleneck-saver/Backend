VANILA_MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
THIRD_PARTY_MIDDLEWARE = ['corsheaders.middleware.CorsMiddleware',
                          'allauth.account.middleware.AccountMiddleware']
MIDDLEWARE = VANILA_MIDDLEWARE + THIRD_PARTY_MIDDLEWARE
