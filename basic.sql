CREATE USER albumator;
CREATE SCHEMA albumator AUTHORIZATION albumator;
CREATE DATABASE albumator;
GRANT CONNECT, USAGE ON DATABASE albumator TO albumator;

-- Start the database server:
--     brew services restart postgresql
--       OR
--     pg_ctl -D /usr/local/var/postgres start
-- Enter a SQL prompt:
--     psql postgres

CREATE TABLE IF NOT EXISTS users (
    user_id serial PRIMARY KEY,
    user_name text NOT NULL UNIQUE,
    date_created date NOT NULL
);

CREATE TABLE IF NOT EXISTS albums (
    album_id serial PRIMARY KEY,
    album_name text,
    user_id integer REFERENCES users ON DELETE CASCADE,
    date_created date NOT NULL,
    date_edited date NOT NULL
);

CREATE TABLE IF NOT EXISTS photos (
    photo_id serial PRIMARY KEY,
    photo_name text,
    user_id integer REFERENCES users ON DELETE CASCADE,
    album_id integer REFERENCES albums ON DELETE CASCADE,
    date_created date NOT NULL,
    date_edited date NOT NULL,
    file_preview text NOT NULL, -- always a JPG
    file_source text UNIQUE NOT NULL -- a RAW file usually, possibly other formats
);

CREATE TABLE IF NOT EXISTS edits (
    edit_id serial PRIMARY KEY,
    edit_name text,
    user_id integer REFERENCES users ON DELETE CASCADE,
    photo_id integer REFERENCES photos ON DELETE CASCADE, -- edits belong to their photo's album
    date_created date NOT NULL,
    date_edited date NOT NULL,
    file_preview text NOT NULL, -- always a JPG
    file_source text UNIQUE NOT NULL -- an XML file usually, possibly JSON
);

-- insert a user
INSERT INTO users (user_name, date_created) VALUES ('jojo', now());

-- insert an album
INSERT INTO albums (
    album_name,
    user_id,
    date_created,
    date_edited
) VALUES (
    'landscapes',
    (SELECT user_id FROM users LIMIT 1),
    now(),
    now()
);

-- insert a photo
INSERT INTO photos (
    photo_name,
    user_id,
    album_id,
    date_created,
    date_edited,
    file_preview,
    file_source
) VALUES (
    'mount haruna',
    (SELECT user_id FROM users LIMIT 1),
    (SELECT album_id FROM albums LIMIT 1),
    now(),
    now(),
    '/path/to/preview.jpg',
    '/path/to/some/file.raw'
);

-- insert an edit
INSERT INTO edits (
    edit_name,
    user_id,
    photo_id,
    date_created,
    date_edited,
    file_preview,
    file_source
) VALUES (
    'My edit',
    (SELECT user_id FROM users LIMIT 1),
    (SELECT photo_id FROM photos LIMIT 1),
    now(),
    now(),
    '/path/to/preview.jpg',
    '/path/to/some/file.xml'
);

-- grab all users
SELECT * FROM users;

-- grab all photos for a user
SELECT * FROM photos WHERE user_id = (SELECT user_id FROM users LIMIT 1);

-- grab all albums for a user
SELECT * FROM albums WHERE user_id = (SELECT user_id FROM users LIMIT 1);

-- grab all photos for an album
SELECT * FROM photos WHERE album_id = (SELECT album_id FROM albums LIMIT 1);

-- count number of photos for a user
SELECT count(*) as count FROM photos WHERE user_id = (SELECT user_id FROM users LIMIT 1);

-- grab all edits for a photo
SELECT * FROM edits WHERE photo_id = (SELECT photo_id FROM photos LIMIT 1);

-- grab all edits for a user
SELECT * FROM edits WHERE user_id = (SELECT user_id FROM users LIMIT 1);

-- delete an edit
DELETE FROM edits WHERE edit_id = (SELECT edit_id FROM edits LIMIT 1);

-- delete a photo
DELETE FROM photos WHERE photo_id = (SELECT photo_id FROM photos LIMIT 1);

-- delete an album
DELETE FROM albums WHERE album_id = (SELECT album_id FROM albums LIMIT 1);

-- delete a user
DELETE FROM users WHERE user_id = (SELECT user_id FROM users LIMIT 1);
