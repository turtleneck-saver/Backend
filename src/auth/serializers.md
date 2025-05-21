### `UserSerializer` 설명

이 코드는 Django Rest Framework(DRF)에서 사용자 모델을 다루는 Serializer임. 특히 **새로운 사용자를 만들 때** 사용함.

```python
from django.contrib.auth.models import User # Django 기본 유저 모델 가져옴
from rest_framework import serializers # DRF 시리얼라이저 기능 임포트


class UserSerializer(serializers.ModelSerializer):
    # User 모델에 맞춰 데이터 변환/검증하는 클래스
    # ModelSerializer라 모델 기반으로 쉽게 만듦

    class Meta:
        # 이 시리얼라이저가 어떤 모델 쓸지, 필드는 뭐 포함할지 설정
        model = User # User 모델 사용
        fields = ('id', 'username', 'password') # id, username, password 필드 사용
        extra_kwargs = {'password': {'write_only': True}}
        # 'password' 필드는 '쓰기 전용'으로 설정함.
        # -> 데이터 받을 땐 password 값 쓸 수 있지만, API 응답으로 내보낼 땐 password 포함 안 됨. (보안 중요!)

    def create(self, validated_data):
        # 시리얼라이저 save() 할 때 새 객체 만드는 로직
        user = User.objects.create_user(**validated_data)
        # validated_data (유효성 검사 통과한 데이터)로 User 객체 만듦.
        # User.objects.create_user()를 쓰면 비밀번호를 자동으로 **안전하게 암호화**해서 저장해 줌!
        # 일반 create() 쓰면 비밀번호가 그대로 저장될 수 있어 위험.

        return user
        # 만들어진 User 객체 반환
```

**결론:**

*   API로 사용자 회원가입/생성 기능을 만들 때 쓰는 시리얼라이저.
*   들어온 `username`, `password` 데이터를 User 모델에 맞게 처리.
*   **가장 중요한 기능**: 입력받은 비밀번호를 `create_user`로 **안전하게 해싱**해서 DB에 저장함.
*   보안 때문에 API 응답에는 비밀번호를 포함하지 않음.
