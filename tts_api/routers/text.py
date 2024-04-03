# pylint: disable=unused-argument
from typing import Optional
from pydantic import BaseModel, Field
from fastapi import APIRouter, status
# from tts_api.exceptions import NotFoundException

router = APIRouter(prefix="/text", tags=["text"])


class TextRequest(BaseModel):
    text: str = Field(min_length=1, examples=["You are awesome !"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def send_text(
        # text_request: TextRequest.text
        text_request: str = Field(min_length=1, examples=["You are awesome !"])
):
    return text_request  # todo: finalize !
