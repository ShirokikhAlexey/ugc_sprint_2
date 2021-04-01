config = {
    "pg_dsn": {
        "host": "localhost",
        "port": 5432,
        "user": "postgres",
        "password": "pass",
    },
    "mongo": {
        "host": "localhost",
        "port": 27017
    },
    "insert_batch_size": 1000,
    "test":
    {
        "users_count": 1000,
        "movies_count": 10000,
        "read_test_count": 10
    }
}