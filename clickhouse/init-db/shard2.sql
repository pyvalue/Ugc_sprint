CREATE DATABASE IF NOT EXISTS shard;

CREATE DATABASE IF NOT EXISTS replica;

CREATE TABLE shard.kafka_movie_view (
      user_id UUID,
      film_id UUID,
      viewed_frame Int32,
      timestamp DateTime('Europe/Moscow'))
      ENGINE = Kafka('localhost:9092', 'mviews', 'frame-viewers-group', 'JSONEachRow');

CREATE MATERIALIZED VIEW consumer TO shard.movie_view
      AS SELECT *
      FROM shard.kafka_movie_view;

CREATE TABLE IF NOT EXISTS shard.movie_view (
      user_id UUID,
      film_id UUID,
      viewed_frame Int32,
      timestamp DateTime('Europe/Moscow'))
      Engine=ReplicatedMergeTree('/clickhouse/tables/shard1/movie_view', 'replica_1') PARTITION BY toYYYYMMDD(event_time) ORDER BY user_id;

CREATE TABLE IF NOT EXISTS replica.movie_view (
      user_id UUID,
      film_id UUID,
      viewed_frame Int32,
      timestamp DateTime('Europe/Moscow'))
      Engine=ReplicatedMergeTree('/clickhouse/tables/shard2/movie_view', 'replica_2') PARTITION BY toYYYYMMDD(event_time) ORDER BY user_id;

CREATE TABLE IF NOT EXISTS default.movie_view (
      user_id UUID,
      film_id UUID,
      viewed_frame Int32,
      timestamp DateTime('Europe/Moscow')) ENGINE = Distributed('company_cluster', '', movie_view, rand());