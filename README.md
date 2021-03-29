# Проектная работа 8 спринта

## Запуск приложения

1. Поднимаем ElasticSearch, Redis, Kafka и API

```bash
docker-compose -f docker-compose.yaml -f kafka/docker-compose.yml up -d --build
```

2. Создаём схему схемы для индексов *movies*, *genres* и *persons* в ElasticSearch.

```bash
/api/utils/create_es_schemas.sh
```

Приложение будет доступно на http://localhost:8888/
OpenAPI схема: http://localhost:8888/api/openapi

## Тестирование

### Функциональные тесты

```bash
PYTHONPATH="api/src" python -m pytest api_tests/functional
```

### Интеграционные тесты

```bash
docker-compose -f api_tests/docker-compose.yaml up -d --build
PYTHONPATH="api/src" python -m pytest api_tests/integration
```

### Construction in Progress

Кафка пока запускается через /kafka/docker-compose.yml

ClickHouse пока запускается через /clickhouse/docker-compose.yml
