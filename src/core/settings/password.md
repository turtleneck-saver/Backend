
# 🔒 Django 비밀번호 유효성 검사기 설정 README

## ✨ 개요

이 문서는 Django 프로젝트의 사용자 비밀번호 유효성 검사기(`AUTH_PASSWORD_VALIDATORS`) 설정을 설명합니다. 이 설정은 사용자가 안전한 비밀번호를 설정하도록 강제하여 계정 보안을 강화하는 데 사용됩니다.

## 🛠️ 비밀번호 유효성 검사기 설정 항목

```python
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]
```

*   **비밀번호 유효성 검사기(Password Validators)**: 사용자 회원가입 또는 비밀번호 변경 시, 입력된 비밀번호가 프로젝트에서 요구하는 보안 기준을 만족하는지 검사하는 일련의 검사기 목록입니다. 이 목록에 정의된 모든 검사기를 통과해야 비밀번호 설정이 완료됩니다.
*   `django.contrib.auth.password_validation.UserAttributeSimilarityValidator`: 사용자 모델의 속성(예: username, first\_name, last\_name, email)과 너무 유사한 비밀번호는 사용하지 못하도록 검사합니다. 개인 정보와 쉽게 연관되는 비밀번호 사용을 방지합니다.
*   `django.contrib.auth.password_validation.MinimumLengthValidator`: 비밀번호의 최소 길이를 검사합니다. 기본적으로 8자 이상을 요구하지만, `OPTIONS`를 통해 최소 길이를 변경할 수 있습니다.
*   `django.contrib.auth.password_validation.CommonPasswordValidator`: 'password123', '111111'과 같이 흔히 사용되어 이미 노출되었을 가능성이 높은 취약한 비밀번호 목록에 포함되어 있는지 검사합니다.
*   `django.contrib.auth.password_validation.NumericPasswordValidator`: 비밀번호 전체가 숫자로만 구성되어 있는지 검사합니다. '12345678'과 같이 추측하기 쉬운 숫자열 비밀번호 사용을 방지합니다.

