import logging

import aioredis
import logstash
import sentry_sdk
import uvicorn as uvicorn
from asgi_request_id import RequestIDMiddleware, get_request_id
from elasticsearch import AsyncElasticsearch
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from typing import Optional
from api.v1 import film, genre, person
from core import config
from core.logger import LOGGING
from db import elastic, redis

sentry_sdk.init(dsn=config.SENTRY_DSN, traces_sample_rate=1.0)

app = FastAPI(
    title=config.PROJECT_NAME,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,

)

app.add_middleware(SentryAsgiMiddleware)


@app.on_event('startup')
async def startup():
    redis.redis = await aioredis.create_redis_pool((config.REDIS_HOST, config.REDIS_PORT), minsize=10, maxsize=20)
    elastic.es = AsyncElasticsearch(
        hosts=[f'{config.ELASTIC_HOST}:{config.ELASTIC_PORT}'])


@app.on_event('shutdown')
async def shutdown():
    redis.redis.close()
    await elastic.es.close()


app.add_middleware(
    RequestIDMiddleware,
    incoming_request_id_header="X-Request-Id",
    prefix="Generated-",
)


class RequestIdFilter(logging.Filter):
    def filter(self, record):
        r_id: Optional[str] = get_request_id()
        if isinstance(r_id, str) and r_id.startswith(prefix="Generated-"):
            r_id = None
        record.request_id = r_id
        return True


#uvicorn.config.logger.addHandler(logging.FileHandler(config.LOGS_PATH, mode="w"))

uvicorn.config.logger.addFilter(RequestIdFilter())

app.include_router(film.router, prefix='/v1/film', tags=['film'])
app.include_router(genre.router, prefix='/v1/genre', tags=['genre'])
app.include_router(person.router, prefix='/v1/person', tags=['person'])

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host=config.APP_HOST,
        port=int(config.APP_PORT),
        log_config=LOGGING,
        log_level=logging.DEBUG,
        lifespan="on"
    )
