# your_app/tasks.py
from celery import shared_task
from .models import Like  # 예시 모델

# 예시: 카운터 값을 증가시키는 비동기 작업

cnt = 0


@shared_task
def increment_like_count(counter_id):
    global cnt
    cnt += 1
    like = Like.objects.get(board_id=counter_id)
    like.like += 1
    like.save()
    print(cnt)
    print(f"카운터 {counter_id} 값을 증가시켰습니다.")
