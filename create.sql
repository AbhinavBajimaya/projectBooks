CREATE TABLE users(
    id SERIAL PRIMARY KEY,
    username VARCHAR UNIQUE NOT NULL,
    email VARCHAR UNIQUE NOT NULL,
    password VARCHAR NOT NULL

);

CREATE TABLE books(
    id SERIAL PRIMARY KEY,
    isbn VARCHAR UNIQUE NOT NULL,
    title VARCHAR NOT NULL,
    author VARCHAR NOT NULL,
    year SMALLINT NOT NULL
);

CREATE TABLE reviews(
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    book_id INTEGER REFERENCES books,
    rating SMALLINT NOT NULL CONSTRAINT invalid_rating CHECK (rating <=5 AND rating >=1),
    review VARCHAR 
);
