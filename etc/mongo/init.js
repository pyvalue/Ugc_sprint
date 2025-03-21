conn = new Mongo();
db = conn.getDB('ugc_movies');

db.createCollection('likes');
db.createCollection('bookmarks');
db.createCollection('reviews');

db.likes.createIndex({ film_id: 1, user_id: 1 }, { unique: true });
db.bookmarks.createIndex({ film_id: 1, user_id: 1 }, { unique: true });
db.reviews.createIndex({ film_id: 1, user_id: 1 }, { unique: true });
