# chatapp/consumers.py 또는 원하는 위치에
import json
from channels.generic.websocket import WebsocketConsumer


class EchoConsumer(WebsocketConsumer):
    def connect(self):
        # 연결 요청이 들어오면 수락!
        self.accept()

    def disconnect(self, close_code):
        # 연결 끊어지면 할 일 (지금은 딱히 없음)
        pass

    def receive(self, text_data):
        # 클라이언트로부터 메시지를 받으면...
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # 받은 메시지를 그대로 클라이언트에게 다시 보내주기!
        self.send(text_data=json.dumps({
            'message': f'Echo: {message}'
        }))
