import os
from logging import config as logging_config

from core.logger import LOGGING

# Применяем настройки логирования
logging_config.dictConfig(LOGGING)
SENTRY_DSN = "https://2505ae73da014cb58f79105054c99444@o558819.ingest.sentry.io/5692867"
LOGSTASH_HOST = os.getenv('LOGSTASH_HOST', 'localhost')

# Название проекта. Используется в Swagger-документации
PROJECT_NAME = os.getenv('PROJECT_NAME', 'movies-api')

# Настройки Redis
REDIS_HOST = os.getenv('REDIS_HOST', '127.0.0.1')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))

# Настройки Elasticsearch
ELASTIC_HOST = os.getenv('ELASTIC_HOST', '127.0.0.1')
ELASTIC_PORT = int(os.getenv('ELASTIC_PORT', 9200))

# Настройки приложения
APP_HOST = os.getenv('APP_HOST', '0.0.0.0')
APP_PORT = os.getenv('APP_PORT', '8888')

# Корень проекта
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
