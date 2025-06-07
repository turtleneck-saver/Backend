# # myapp/views.py 파일에 작성한다고 가정해볼게!
# from django.db import transaction
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework.permissions import AllowAny, IsAuthenticated
# from .models import Like
# current_count = 0  # 전역 변수로 카운트 값을 저장 (간단 예시용)

# # # APIView를 상속받아서 View 클래스를 만들어줘!


# # class CounterAPIView(APIView):
# #     permission_classes = [AllowAny]
# #     # GET 요청을 받으면 현재 카운트 값을 돌려줄 거야!

# #     def get(self, request):
# #         like = Like.objects.get(board_id='1')
# #         current_count = like.like
# #         return Response({"count": current_count}, status=status.HTTP_200_OK)

# #     # POST 요청을 받으면 카운트 값을 1 증가시키고, 증가된 값을 돌려줄 거야!
# #     def post(self, request):

# #         like = Like.objects.get(board_id='1')
# #         like.like += 1
# #         current_count = like.like
# #         like.save()

# #         # 증가된 카운트 값을 JSON 형태로 응답!
# #         return Response({"count": current_count}, status=status.HTTP_200_OK)

# #     # 만약 PUT, DELETE 같은 다른 요청도 처리하고 싶으면 해당 메서드를 추가로 정의하면 돼!
# #     # def put(self, request):
# #     #    ...


# class CounterAPIView(APIView):
#     permission_classes = [AllowAny]

#     def get(self, request):
#         # 읽기만 할 때는 트랜잭션 커밋이 필요 없음 (Django가 자동 처리)
#         like = Like.objects.get(board_id='1')
#         current_count = like.like
#         return Response({"count": current_count}, status=status.HTTP_200_OK)

#     def post(self, request):

#         with transaction.atomic():
#             like = Like.objects.get(board_id='1')
#             like.like += 1
#             like.save()
#             current_count = like.like

#         return Response({"count": current_count}, status=status.HTTP_200_OK)
# your_app/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .tasks import increment_like_count  # increment_like_count task 임포트
from .models import Like  # Like 모델 임포트


class CounterAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        # 읽기 작업은 그대로 유지
        try:
            like = Like.objects.get(board_id='1')
            current_count = like.like
            return Response({"count": current_count}, status=status.HTTP_200_OK)
        except Like.DoesNotExist:
            return Response({"count": 0}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        # Celery task 호출
        increment_like_count.delay(
            '1')  # 비동기 task 실행, board_id 전달
        # 202 Accepted 응답
        return Response({"message": "좋아요 수 증가 요청이 처리되었습니다."}, status=status.HTTP_202_ACCEPTED)
