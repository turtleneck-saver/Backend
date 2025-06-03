# myapp/views.py 파일에 작성한다고 가정해볼게!
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
# ⚠️ 주의: 실제 서비스에서는 이렇게 메모리에 저장하면 안 돼요!
# 서버가 재시작되거나 여러 워커가 돌면 값이 초기화되거나 동기화 문제가 생길 수 있어요.
# 실제로는 데이터베이스나 캐시 저장소(Redis 등)를 사용해야 합니다!
current_count = 0  # 전역 변수로 카운트 값을 저장 (간단 예시용)

# APIView를 상속받아서 View 클래스를 만들어줘!


class CounterAPIView(APIView):
    permission_classes = [AllowAny]
    # GET 요청을 받으면 현재 카운트 값을 돌려줄 거야!

    def get(self, request):
        global current_count  # 전역 변수 current_count를 사용하겠다고 선언

        # 현재 카운트 값을 JSON 형태로 응답!
        # Response 객체를 사용하면 DRF가 알아서 JSON 형태로 변환해줘!
        return Response({"count": current_count}, status=status.HTTP_200_OK)

    # POST 요청을 받으면 카운트 값을 1 증가시키고, 증가된 값을 돌려줄 거야!
    def post(self, request):
        global current_count  # 전역 변수 current_count를 사용하겠다고 선언

        # 카운트 값을 1 증가!
        current_count += 1

        # 증가된 카운트 값을 JSON 형태로 응답!
        return Response({"count": current_count}, status=status.HTTP_200_OK)

    # 만약 PUT, DELETE 같은 다른 요청도 처리하고 싶으면 해당 메서드를 추가로 정의하면 돼!
    # def put(self, request):
    #    ...
