import pytest
import json
from channels.testing import WebsocketCommunicator
from .consumers import ChatConsumer


@pytest.mark.asyncio
async def test_chat_consumer():
    communicator = WebsocketCommunicator(
        ChatConsumer.as_asgi(), "/ws/chat/testroom/")
    connected, subprotocol = await communicator.connect()
    assert connected is True

    await communicator.send_to(text_data=json.dumps({"message": "Hello!"}))
    response = await communicator.receive_from()
    assert json.loads(response)["message"] == "Hello!"

    await communicator.disconnect()
