CREATE TABLE IF NOT EXISTS users (
  	id uuid PRIMARY KEY);

CREATE TABLE IF NOT EXISTS movies (
  	id uuid PRIMARY KEY);

CREATE TABLE IF NOT EXISTS likes (
  	id uuid PRIMARY KEY,
  	user_id uuid,
  	movie_id uuid,
  	FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (movie_id) REFERENCES movies(id),
    num_like integer CONSTRAINT positive_num_like CHECK (num_like > 0),
    created timestamp,
    modified timestamp);

CREATE TABLE IF NOT EXISTS bookmarks (
  	id uuid PRIMARY KEY,
  	user_id uuid,
  	movie_id uuid,
  	FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (movie_id) REFERENCES movies(id),
    created timestamp);

CREATE TABLE IF NOT EXISTS reviews (
  	id uuid PRIMARY KEY,
  	user_id uuid,
  	movie_id uuid,
  	FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (movie_id) REFERENCES movies(id),
    review text,
    created timestamp,
    modified timestamp);