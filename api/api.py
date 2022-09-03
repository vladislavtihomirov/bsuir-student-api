import typing

from fastapi import APIRouter, Depends
from starlette.responses import JSONResponse

from api.endpoints import auth


class StatusResponse(JSONResponse):
    def render(self, content: typing.Any, *args, **kwargs) -> bytes:
        content = {
            "data": content,
            "status": "ok"
        }
        return super().render(content)


api_router = APIRouter(default_response_class=StatusResponse)


@api_router.get('ping')
def pong():
    return pong


api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
