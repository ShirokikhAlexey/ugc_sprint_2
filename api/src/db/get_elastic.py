from elasticsearch import AsyncElasticsearch

es: AsyncElasticsearch = None  # type: ignore


# Функция понадобится при внедрении зависимостей


async def get_elastic() -> AsyncElasticsearch:
    return es
