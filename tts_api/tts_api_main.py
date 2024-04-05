"""
Text provider API.

This project supposed to be used for the text input and providing the text to the TTS model
"""
from fastapi import FastAPI
from starlette.responses import JSONResponse
from starlette.requests import Request

from tts_api.routers import text

app = FastAPI(
    title="TTS api",
    description="""
    TTS API.

    Application created for interacting with TTS model via API
    """,
)

app.include_router(text.router)


@app.exception_handler(Exception)
async def exception_handler(
    request: Request, exc: Exception
):  # pylint: disable=unused-argument
    return JSONResponse(
        status_code=500,
        content={"message": f"Oops!. Internal server error with message {exc}"},
    )
