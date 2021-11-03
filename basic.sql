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

-- Destroy all tables and rows:
--     TRUNCATE edit, photo, album, account RESTART IDENTITY CASCADE;
--     DROP TABLE edit_contributor, photo_contributor, album_access, edit, photo, album, account CASCADE;
--     DROP TYPE permission, contributor;

CREATE TYPE permission AS ENUM ('none', 'read', 'add', 'modify');

-- Contributor represents the typed contribution of a person toward producing a resource:
CREATE TYPE contributor AS ENUM (
    'other',
    'assistant',
    'model',
    'technician',
    'editor',
    'photographer',
    'director'
);

CREATE TABLE IF NOT EXISTS account (
    account_id SERIAL PRIMARY KEY,
    account_name TEXT NOT NULL UNIQUE,
    created_at TIMESTAMP NOT NULL DEFAULT now(),
    edited_at TIMESTAMP NOT NULL DEFAULT now(),
    deleted_at TIMESTAMP
);

-- only the album's owner can delete it
CREATE TABLE IF NOT EXISTS album (
    album_id SERIAL PRIMARY KEY,
    owner_id INTEGER NOT NULL REFERENCES account ON UPDATE CASCADE ON DELETE CASCADE,
    album_name TEXT NOT NULL,
    album_desc TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT now(),
    edited_at TIMESTAMP NOT NULL DEFAULT now()
);

-- a photo can belong to many albums but can only be deleted
-- by its owner (account_id)
CREATE TABLE IF NOT EXISTS photo (
    photo_id SERIAL PRIMARY KEY,
    account_id INTEGER NOT NULL REFERENCES account ON UPDATE CASCADE ON DELETE CASCADE,
    photo_name TEXT NOT NULL,
    photo_desc TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT now(),
    edited_at TIMESTAMP NOT NULL DEFAULT now(),
    file_preview TEXT NOT NULL, -- always an HEIC file
    file_source TEXT UNIQUE NOT NULL -- RAW, CR2, TIFF, JPG, etc
);

-- track which albums each photo belongs to
CREATE TABLE IF NOT EXISTS photo_album (
    photo_id INTEGER NOT NULL REFERENCES photo ON UPDATE CASCADE ON DELETE CASCADE,
    album_id INTEGER NOT NULL REFERENCES album ON UPDATE CASCADE ON DELETE CASCADE,
    PRIMARY KEY (photo_id, album_id)
);

CREATE TABLE IF NOT EXISTS edit (
    edit_id SERIAL PRIMARY KEY,
    edit_name TEXT,
    edit_desc TEXT,
    photo_id INTEGER REFERENCES photo ON UPDATE CASCADE ON DELETE CASCADE, -- edits belong to their photo's album
    created_at TIMESTAMP NOT NULL DEFAULT now(),
    edited_at TIMESTAMP NOT NULL DEFAULT now(),
    file_preview TEXT NOT NULL, -- always an HEIC file
    file_source TEXT UNIQUE NOT NULL -- XML, JSON, YAML, etc
);

-- track account permissions for modifying the contents of each album
CREATE TABLE IF NOT EXISTS album_access (
    account_id INTEGER NOT NULL REFERENCES account ON UPDATE CASCADE ON DELETE CASCADE,
    album_id INTEGER NOT NULL REFERENCES album ON UPDATE CASCADE ON DELETE CASCADE,
    PRIMARY KEY (account_id, album_id),
    permission PERMISSION NOT NULL DEFAULT 'none'
);

-- track contributors for each photo
CREATE TABLE IF NOT EXISTS photo_contributor (
    account_id INTEGER NOT NULL REFERENCES account ON UPDATE CASCADE ON DELETE CASCADE,
    photo_id INTEGER NOT NULL REFERENCES photo ON UPDATE CASCADE ON DELETE CASCADE,
    PRIMARY KEY (account_id, photo_id),
    contributor CONTRIBUTOR NOT NULL DEFAULT 'other'
);

-- track contributors for each edit
CREATE TABLE IF NOT EXISTS edit_contributor (
    account_id INTEGER NOT NULL REFERENCES account ON UPDATE CASCADE ON DELETE CASCADE,
    edit_id INTEGER NOT NULL REFERENCES edit ON UPDATE CASCADE ON DELETE CASCADE,
    PRIMARY KEY (account_id, edit_id),
    contributor CONTRIBUTOR NOT NULL DEFAULT 'other'
);

-- insert accounts
INSERT INTO account (account_name) VALUES ('jojo'), ('chumpy'), ('tarzan');

-- insert an album and associate privileges with accounts
INSERT INTO album (album_name, album_desc, owner_id) VALUES
    ('Landscapes', 'Photos of mountains mostly', 1);
INSERT INTO album_access (account_id, album_id, permission) VALUES (1, 1, 'modify');
INSERT INTO album_access (account_id, album_id, permission) VALUES (2, 1, 'add');

-- insert photo, associate a contributor with it, and add it to an album
INSERT INTO photo (
    photo_name,
    file_preview,
    file_source
) VALUES (
    'mount haruna',
    '/path/to/preview.jpg',
    '/path/to/some/file.raw'
);
INSERT INTO photo_contributor (account_id, photo_id, contributor) VALUES (1, 1, 'photographer');
INSERT INTO photo_album (photo_id, album_id) VALUES (1, (SELECT album_id FROM album LIMIT 1));

-- repeat for another photo with more contributors
INSERT INTO photo (
    photo_name,
    album_id,
    file_preview,
    file_source
) VALUES (
    'neander valley',
    (SELECT album_id FROM album LIMIT 1),
    '/path/to/another-preview.jpg',
    '/path/to/some/another-file.raw'
);
INSERT INTO photo_contributor (account_id, photo_id, contributor) VALUES (2, 2, 'photographer');
INSERT INTO photo_contributor (account_id, photo_id, contributor) VALUES (1, 2, 'director');
INSERT INTO photo_contributor (account_id, photo_id, contributor) VALUES (3, 2, 'editor');
INSERT INTO photo_album (photo_id, album_id) VALUES (2, (SELECT album_id FROM album LIMIT 1));

-- insert an edit and associate ownership
INSERT INTO edit (
    photo_id,
    edit_name,
    file_preview,
    file_source
) VALUES (
    1,
    'My edit',
    '/path/to/preview.jpg',
    '/path/to/some/file.xml'
);
INSERT INTO edit_contributor (account_id, edit_id, contributor) VALUES (1, 1, 'editor');

-- grab all accounts
SELECT account_id, account_name, created_at FROM account WHERE deleted_at IS NULL;

-- grab all albums for an account
SELECT a.album_id, a.album_name, a.album_desc, a.created_at, a.edited_at FROM album_access AS a_a
JOIN album AS a ON a_a.album_id = a.album_id
WHERE a_a.account_id = (SELECT account_id FROM account WHERE deleted_at IS NULL LIMIT 1);

-- grab all photos for an account
SELECT p.photo_id, p.photo_name, p.photo_desc, p.created_at, p.edited_at, a_p.contributor FROM photo_contributor AS a_p
JOIN photo AS p ON a_p.photo_id = p.photo_id
WHERE a_p.account_id = (SELECT account_id FROM account WHERE deleted_at IS NULL LIMIT 1);

-- grab all edits for an account
SELECT e.edit_id, e.edit_name, e.edit_desc, e.created_at, e.edited_at, a_e.contributor FROM edit_contributor AS a_e
JOIN edit AS e ON a_e.edit_id = e.edit_id
WHERE a_e.account_id = (SELECT account_id FROM account WHERE deleted_at IS NULL LIMIT 1);

-- grab all editors for an album
SELECT account_id, account_name, permission FROM (
    SELECT a.account_id, a.account_name, a.deleted_at, a_a.permission FROM album_access AS a_a
    JOIN account AS a ON a_a.account_id = a.account_id
    WHERE a.deleted_at IS NULL
    AND a_a.album_id = (SELECT album_id FROM album LIMIT 1)
    AND a_a.permission >= 'add'
) AS accounts WHERE deleted_at IS NULL;

-- grab all contributors for a photo
SELECT account_id, account_name, contributor FROM (
    SELECT a.account_id, a.account_name, a.deleted_at, a_p.contributor FROM photo_contributor AS a_p
    JOIN account AS a ON a_p.account_id = a.account_id
    WHERE a.deleted_at IS NULL
    AND a_p.photo_id = (SELECT photo_id FROM photo LIMIT 1)
) AS accounts WHERE deleted_at IS NULL;

-- grab all contributors for an edit
SELECT account_id, account_name, contributor FROM (
    SELECT a.account_id, a.account_name, a.deleted_at, a_e.contributor FROM edit_contributor AS a_e
    JOIN account AS a ON a_e.account_id = a.account_id
    WHERE a.deleted_at IS NULL
    AND a_e.edit_id = (SELECT edit_id FROM edit LIMIT 1)
) AS accounts WHERE deleted_at IS NULL;

-- grab all photos for an album
SELECT photo_id, photo_name, created_at, edited_at, file_preview, file_source
FROM photo WHERE album_id = (SELECT album_id FROM album LIMIT 1);

-- count number of photos for an account
SELECT count(*) as photo_count FROM photo_contributor WHERE account_id = (
    SELECT account_id FROM account WHERE deleted_at IS NULL LIMIT 1
);

-- grab all edits for a photo
SELECT edit_id, edit_name, created_at, edited_at, file_preview, file_source
FROM edit WHERE photo_id = (SELECT photo_id FROM photo LIMIT 1);

-- delete an edit
DELETE FROM edit WHERE edit_id = (SELECT edit_id FROM edit LIMIT 1);

-- delete a photo
DELETE FROM photo WHERE photo_id = (SELECT photo_id FROM photo LIMIT 1);

-- delete an album
DELETE FROM album WHERE album_id = (SELECT album_id FROM album LIMIT 1);

-- delete an account (set flag only)
UPDATE account SET deleted_at = now() WHERE account_id = (
    SELECT account_id FROM account WHERE deleted_at IS NULL LIMIT 1
);
