#!/usr/bin/env bash
clickhouse-client "CREATE DATABASE shard;"
clickhouse-client "CREATE DATABASE replica1;"

clickhouse-client "CREATE DATABASE replica2;"

clickhouse-client "CREATE TABLE shard.views (user_id String, movie_id String, value_timestamp DateTime) \
Engine=ReplicatedMergeTree('/clickhouse/tables/shard3/views', 'replica_1') \
PARTITION BY toYYYYMMDD(value_timestamp) ORDER BY value_timestamp;"

clickhouse-client "CREATE TABLE replica1.views (user_id String, movie_id String, value_timestamp DateTime) \
Engine=ReplicatedMergeTree('/clickhouse/tables/shard1/views', 'replica_2') \
PARTITION BY toYYYYMMDD(value_timestamp) ORDER BY value_timestamp;"

clickhouse-client "CREATE TABLE replica2.views (user_id String, movie_id String, value_timestamp DateTime) \
Engine=ReplicatedMergeTree('/clickhouse/tables/shard2/views', 'replica_3') \
PARTITION BY toYYYYMMDD(value_timestamp) ORDER BY value_timestamp;"

clickhouse-client "CREATE TABLE default.views (user_id String, movie_id String, value_timestamp DateTime) \
ENGINE = Distributed('company_cluster', '', views, rand());"