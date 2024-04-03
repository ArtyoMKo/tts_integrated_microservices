# pylint: disable=unused-argument
from pydantic import BaseModel, Field
from fastapi import APIRouter, status
# from tts_api.exceptions import NotFoundException

from pulsar_provider import PulsarProvider

router = APIRouter(prefix="/text", tags=["text"])


text_pulsar_provider = PulsarProvider()


class TextRequest(BaseModel):
    text: str = Field(min_length=1, examples=["You are awesome !"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def send_text(
        text_request: TextRequest
):
    return text_request.text  # todo: finalize !
