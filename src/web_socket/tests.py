

import pytest
import json
from channels.testing import WebsocketCommunicator
from .consumers import EchoConsumer


@pytest.mark.asyncio
async def test_echo_consumer_receives_and_sends_message():
    communicator = WebsocketCommunicator(
        EchoConsumer.as_asgi(), "/ws/chat/testroom/")
    try:
        print('안녕')
        connected, subprotocol = await communicator.connect()
        assert connected is True

        await communicator.send_to(text_data=json.dumps({"message": "Hello!"}))
        response = await communicator.receive_from()
        assert json.loads(response)["message"] == "Echo: Hello!"

        await communicator.disconnect()
    except Exception as e:
        print(f"테스트 중 에러 발생: {e}")
        assert False, f"테스트 실패: {e}"
