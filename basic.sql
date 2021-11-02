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
--     DROP TABLE account_edit, account_photo, account_album, edit, photo, album, account CASCADE;
--     DROP TYPE role, contributor;

-- Role represents the cumulative privileges to view, update, and delete a resource:
--  idx  role     privilege
-- +---+--------+----------+
-- | 0 | none   | none     |
-- | 1 | viewer | read     |
-- | 2 | editor | write    |
-- | 3 | owner  | delete   |
-- +---+--------+----------+
CREATE TYPE role AS ENUM ('none', 'viewer', 'editor', 'owner');

-- Contributor represents the typed contribution of a person toward producing a resource:
CREATE TYPE contributor AS ENUM ('other', 'assistant', 'model', 'technician', 'editor', 'photographer', 'director');

CREATE TABLE IF NOT EXISTS account (
    account_id SERIAL PRIMARY KEY,
    account_name TEXT NOT NULL UNIQUE,
    created_at TIMESTAMP NOT NULL DEFAULT now(),
    edited_at TIMESTAMP NOT NULL DEFAULT now(),
    deleted_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS album (
    album_id SERIAL PRIMARY KEY,
    album_name TEXT NOT NULL,
    album_desc TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT now(),
    edited_at TIMESTAMP NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS photo (
    photo_id SERIAL PRIMARY KEY,
    photo_name TEXT NOT NULL,
    photo_desc TEXT,
    album_id INTEGER REFERENCES album ON UPDATE CASCADE ON DELETE CASCADE,
    created_at TIMESTAMP NOT NULL DEFAULT now(),
    edited_at TIMESTAMP NOT NULL DEFAULT now(),
    file_preview TEXT NOT NULL, -- always an HEIC file
    file_source TEXT UNIQUE NOT NULL -- RAW, CR2, TIFF, JPG, etc
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

-- map accounts to albums (many-many) with role recorded per mapping
CREATE TABLE IF NOT EXISTS account_album (
    account_id INTEGER NOT NULL REFERENCES account ON UPDATE CASCADE ON DELETE CASCADE,
    album_id INTEGER NOT NULL REFERENCES album ON UPDATE CASCADE ON DELETE CASCADE,
    role ROLE NOT NULL DEFAULT 'none'
);

-- map accounts to photos (many-many) with contributor status recorded per mapping
CREATE TABLE IF NOT EXISTS account_photo (
    account_id INTEGER NOT NULL REFERENCES account ON UPDATE CASCADE ON DELETE CASCADE,
    photo_id INTEGER NOT NULL REFERENCES photo ON UPDATE CASCADE ON DELETE CASCADE,
    contributor CONTRIBUTOR NOT NULL DEFAULT 'other'
);

-- map accounts to edits (many-many) with contributor status recorded per mapping
CREATE TABLE IF NOT EXISTS account_edit (
    account_id INTEGER NOT NULL REFERENCES account ON UPDATE CASCADE ON DELETE CASCADE,
    edit_id INTEGER NOT NULL REFERENCES edit ON UPDATE CASCADE ON DELETE CASCADE,
    contributor CONTRIBUTOR NOT NULL DEFAULT 'other'
);

-- insert accounts
INSERT INTO account (account_name) VALUES ('jojo'), ('chumpy'), ('tarzan');

-- insert an album and associate privileges with accounts
INSERT INTO album (album_name) VALUES ('landscapes');
INSERT INTO account_album (account_id, album_id, role) VALUES (1, 1, 'owner');
INSERT INTO account_album (account_id, album_id, role) VALUES (2, 1, 'editor');

-- insert photo and associate contributor status for an account
INSERT INTO photo (
    photo_name,
    album_id,
    file_preview,
    file_source
) VALUES (
    'mount haruna',
    (SELECT album_id FROM album LIMIT 1),
    '/path/to/preview.jpg',
    '/path/to/some/file.raw'
);
INSERT INTO account_photo (account_id, photo_id, contributor) VALUES (1, 1, 'photographer');

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
INSERT INTO account_photo (account_id, photo_id, contributor) VALUES (2, 2, 'photographer');
INSERT INTO account_photo (account_id, photo_id, contributor) VALUES (1, 2, 'director');
INSERT INTO account_photo (account_id, photo_id, contributor) VALUES (3, 2, 'editor');

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
INSERT INTO account_edit (account_id, edit_id, contributor) VALUES (1, 1, 'editor');

-- grab all accounts
SELECT account_id, account_name, created_at FROM account WHERE deleted_at IS NULL;

-- grab all albums for an account
SELECT a.album_id, a.album_name, a.album_desc, a.created_at, a.edited_at FROM account_album AS a_a
JOIN album AS a ON a_a.album_id = a.album_id
WHERE a_a.account_id = (SELECT account_id FROM account WHERE deleted_at IS NULL LIMIT 1);

-- grab all photos for an account
SELECT p.photo_id, p.photo_name, p.photo_desc, p.created_at, p.edited_at, a_p.contributor FROM account_photo AS a_p
JOIN photo AS p ON a_p.photo_id = p.photo_id
WHERE a_p.account_id = (SELECT account_id FROM account WHERE deleted_at IS NULL LIMIT 1);

-- grab all edits for an account
SELECT e.edit_id, e.edit_name, e.edit_desc, e.created_at, e.edited_at, a_e.contributor FROM account_edit AS a_e
JOIN edit AS e ON a_e.edit_id = e.edit_id
WHERE a_e.account_id = (SELECT account_id FROM account WHERE deleted_at IS NULL LIMIT 1);

-- grab all editors for an album
SELECT account_id, account_name, role FROM (
    SELECT a.account_id, a.account_name, a.deleted_at, a_a.role FROM account_album AS a_a
    JOIN account AS a ON a_a.account_id = a.account_id
    WHERE a.deleted_at IS NULL
    AND a_a.album_id = (SELECT album_id FROM album LIMIT 1)
    AND a_a.role >= 'editor'
) AS accounts WHERE deleted_at IS NULL;

-- grab all contributors for a photo
SELECT account_id, account_name, contributor FROM (
    SELECT a.account_id, a.account_name, a.deleted_at, a_p.contributor FROM account_photo AS a_p
    JOIN account AS a ON a_p.account_id = a.account_id
    WHERE a.deleted_at IS NULL
    AND a_p.photo_id = (SELECT photo_id FROM photo LIMIT 1)
) AS accounts WHERE deleted_at IS NULL;

-- grab all contributors for an edit
SELECT account_id, account_name, contributor FROM (
    SELECT a.account_id, a.account_name, a.deleted_at, a_e.contributor FROM account_edit AS a_e
    JOIN account AS a ON a_e.account_id = a.account_id
    WHERE a.deleted_at IS NULL
    AND a_e.edit_id = (SELECT edit_id FROM edit LIMIT 1)
) AS accounts WHERE deleted_at IS NULL;

-- grab all photos for an album
SELECT photo_id, photo_name, created_at, edited_at, file_preview, file_source
FROM photo WHERE album_id = (SELECT album_id FROM album LIMIT 1);

-- count number of photos for an account
SELECT count(*) as photo_count FROM account_photo WHERE account_id = (
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
