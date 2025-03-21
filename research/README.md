# Research Results

### ClickHouse

* Total INSERT time (10 000 000):
375.8195
* Total INSERT time (100 000):
3.9073

* Total SELECT time (SELECT 100 from 10 000 000):
45.2239

### Vertica

* Total INSERT time (10 000 000):
972.6340
* Total INSERT time (100 000):
7.6928

* Total SELECT time (SELECT 100 from 10 000 000):
6.1624

### Aggregation functions (for 100 000 elements)
| **Select**           | **Clickhouse** | **Clickhouse (Realtime)** | **Vertica** | **Vertica (Realtime)** |
|----------------------|----------------|---------------------------|-------------|------------------------|
| **100_elements**     | 0.7906         | 1.2480                    | 0.8911      | 0.9675                 |
| **avg_viewed_frame** | 0.1973         | 0.2109                    | 0.0533      | 0.0606                 |
| **max_viewed_frame** | 0.0061         | 0.0075                    | 0.0101      | 0.0121                 |
| **count_users**      | 0.1779         | 0.1965                    | 0.0924      | 0.0988                 |
| **count_movies**     | 0.0066         | 0.0079                    | 0.0139      | 0.0236                 |