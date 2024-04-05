# pylint: disable=unused-argument
from pydantic import BaseModel, Field  # pylint: disable=no-name-in-module
from fastapi import APIRouter, status
from pulsar.schema import StringSchema

from pulsar_provider import PulsarProvider

router = APIRouter(prefix="/text", tags=["text"])


text_pulsar_provider = PulsarProvider()
text_producer = text_pulsar_provider.create_producer("row_text", StringSchema())


class TextRequest(BaseModel):
    text: str = Field(min_length=1, examples=["You are awesome !"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def send_text(text_request: TextRequest):
    text_producer.send_async(
        text_request.text, callback=text_pulsar_provider.send_callback
    )
    return text_request.text
