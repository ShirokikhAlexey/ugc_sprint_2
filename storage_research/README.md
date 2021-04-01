## Исследование по выбору хранилища для лайков

## Тестируемые базы
Выбирать будем между двумя базами Postgresql и mongodb

## Объем данных
Предполагаем, что в нашем кинотеатре 1000 пользоватлей и 10000 фильмов.
Каждый пользователь поставил оценку каждому фильму.
Всего записей для теста 10 000 000.

## Запуск инфраструктуры
### Характеристики машины
RAM - 15,5 GiB
Procssor - Intel® Core™ i7-8565U CPU @ 1.80GHz × 8
OS - Ubuntu 20.04
### Поднимаем кластер mongodb
Выполняем команды внутри storage_research/mongo_cluster
```bash
docker-compose -f config-servers.yml -f first-shards.yml -f mongo-routers.yml -f second-shard.yml up -d --build
```
После того как контейнеры подняты, выполним настройку кластера
```bash
./prepare-mongo.sh
```

### Поднимаем кластер postgresql
Выполняем команды внутри storage_research/pg_cluster
```bash
docker-compose up -d --build
```

## Запуск тестов

### Генерируем данные
Количество данных конфигурится в файле config.py

1) Устанавливаем зависимости из requirements.txt
2) Запускаем генерацию данных для mongodb
```bash
python3 generate_mongo_data.py
```
3) Запускаем генерацию данных для Postgresql
```bash
python3 generate_pg_data.py
```

### Запуск тестов
1) Запуск для mongodb
```bash
ptyhon3 read_data_mongo.py
```

2) Запуск для postgresql
```bash
ptyhon3 read_data_pg.py
```

## Результаты
Все заросы выполняли 10 раз, и по выборке находили среднее,максимальное и минмальное значение времени выполнения.

### Результат для mongodb
```
TESTS COUNT:  10
----------------------------------------
movie avg rating query time stats
MAX:  7.875 MIN:  6.791 MEAN:  7.424
----------------------------------------
movie rating count query time stats
MAX:  7.758 MIN:  6.863 MEAN:  7.122
----------------------------------------
movie liked by user query time stats
MAX:  7.485 MIN:  6.336 MEAN:  6.944
----------------------------------------
```

### Результат для postgresql
```
TESTS COUNT:  10
----------------------------------------
movie avg rating query time stats
MAX:  0.601 MIN:  0.323 MEAN:  0.356
----------------------------------------
movie rating count query time stats
MAX:  0.378 MIN:  0.315 MEAN:  0.328
----------------------------------------
movie liked by user query time stats
MAX:  0.315 MIN:  0.298 MEAN:  0.304
----------------------------------------
```

### Выводы
В текущей конфигурации кластеров postgresql выглядит намнонго лучше mongodb.
