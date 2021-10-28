CREATE TABLE users (
    user_id serial PRIMARY KEY,
    user_name text NOT NULL UNIQUE,
    date_created date NOT NULL
);

CREATE TABLE albums (
    album_id serial PRIMARY KEY,
    album_name text,
    date_created date NOT NULL,
    date_edited date NOT NULL
);

CREATE TABLE photos (
    photo_id serial PRIMARY KEY,
    photo_name text,
    date_created date NOT NULL,
    date_edited date NOT NULL,
    file_preview text NOT NULL, -- always a JPG
    file_source text UNIQUE NOT NULL -- a RAW file usually, possibly other formats
);

CREATE TABLE edits (
    edit_id serial PRIMARY KEY,
    edit_name text,
    date_created date NOT NULL,
    date_edited date NOT NULL,
    file_preview text NOT NULL, -- always a JPG
    file_source text UNIQUE NOT NULL -- an XML file usually, possibly JSON
);

CREATE TABLE users_albums (
    user_id integer REFERENCES users ON DELETE CASCADE,
    album_id integer REFERENCES albums ON DELETE CASCADE,
    CONSTRAINT users_albums_id PRIMARY KEY (user_id, album_id)
);

CREATE TABLE users_photos (
    user_id integer REFERENCES users ON DELETE CASCADE,
    photo_id integer REFERENCES photos ON DELETE CASCADE,
    CONSTRAINT users_photos_id PRIMARY KEY (user_id, photo_id)
);

CREATE TABLE users_edits (
    user_id integer REFERENCES users ON DELETE CASCADE,
    edit_id integer REFERENCES edits ON DELETE CASCADE,
    CONSTRAINT users_edits_id PRIMARY KEY (user_id, edit_id)
);

CREATE TABLE albums_photos (
    album_id integer REFERENCES albums ON DELETE CASCADE,
    photo_id integer REFERENCES photos ON DELETE CASCADE,
    CONSTRAINT albums_photos_id PRIMARY KEY (album_id, photo_id)
);

CREATE TABLE photos_edits (
    photo_id integer REFERENCES photos ON DELETE CASCADE,
    edit_id integer REFERENCES edits ON DELETE CASCADE,
    CONSTRAINT photos_edits_id PRIMARY KEY (photo_id, edit_id)
);

-- insert a user
INSERT INTO users (user_name, date_created) VALUES ('jojo', now());

-- insert an album

-- insert a photo

