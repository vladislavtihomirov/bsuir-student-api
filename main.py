import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from api.api import api_router

app = FastAPI(
    title="BSUIR-Student-api",
    description="FastAPI + SQLAlchemy + python 3.8",
    version='v1.0.1',
    docs_url="/api/v1/docs",
    openapi_url="/api/v1/openapi.json"
)


origins = [
    '*'
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix='/api/v1')


if __name__ == '__main__':
    uvicorn.run('main:app', host="0.0.0.0", port=3000, log_level='debug', workers=20)
