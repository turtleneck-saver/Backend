# chatapp/routing.py
from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/$',
            consumers.ChatConsumer.as_asgi()),  # 웹소켓 연결 엔드포인트 설정
]
