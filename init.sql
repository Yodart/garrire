
CREATE TABLE rooms
(
    id SERIAL PRIMARY KEY,
    name VARCHAR(80)
);
CREATE TABLE users
(
    id SERIAL PRIMARY KEY,
    username VARCHAR
(30),
    password VARCHAR
(80),
    joined TIMESTAMP DEFAULT NOW
()
);

CREATE TABLE messages
(
    id SERIAL PRIMARY KEY,
    content VARCHAR(1000),
    username VARCHAR(80),
    timestamp TIMESTAMP DEFAULT NOW(),
    room VARCHAR(80)
);

INSERT INTO rooms
    (name)
VALUES
    ('marketing'),
    ('engineering'),
    ('sports'),
    ('general')