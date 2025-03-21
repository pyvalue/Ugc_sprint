# Research Results for MongoDB

### To check results

 Raise the claster:
```
docker-compose up --build
```

Set up the cluster:
```
make init
```

### Results
All researches were carried out with the following parameters to reproduce the actual load on DB:
```
Users: 1000
Movies: 100000
Docs: 1000000 (in every collection: likes, bookmarks, reviews)
```

- Average select time for a list of liked movies for 1 user - 3.74 ms
- Average select time for the number of likes for 1 movie - 28.42 ms
- Average select time for a list of bookmarks for 1 user - 3.35 ms
- Average select time for avg numbers of likes for 1 movie - 24.55 ms
- Online insert + select time for 1 document: 0.008 ms

The average time was calculated on the basis of 100 repetitions for each parameter.

# Research Results for Postges

### To check results

 Raise Postgres:
```
docker-compose up --build
```


### Results
All researches were carried out with the following parameters to reproduce the actual load on DB:
```
Users: 1000
Movies: 100000
Docs: 1000000 (in every collection: likes, bookmarks, reviews)
```

- Average select time for a list of liked movies for 1 user - 8.08 ms
- Average select time for the number of likes for 1 movie - 8.35 ms
- Average select time for a list of bookmarks for 1 user - 7.79 ms
- Average select time for avg numbers of likes for 1 movie - 8.43 ms
- Online insert + select time for 1 document: 0.099 ms

The average time was calculated on the basis of 100 repetitions for each parameter.

# Mongo (NoSQL) vs Postges (SQL)

| **Select**                      | **Mongo** | **Postgres** |
|---------------------------------|-----------|--------------|
| **List of user's liked movies** | 3.74 ms   | 8.08 ms      |
| **Num of user's likes**         | 28.42 ms  | 8.35 ms      |
| **List of user's bookmarks**    | 3.35 ms   | 7.79 ms      |
| **Avg movie's likes**           | 24.55 ms  | 8.43 ms      |
| **Insert + Select**             | 0.008 ms  | 0.099 ms     |

Mongo does better with read requests, while Postgres works well with aggregate functions.