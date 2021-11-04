CREATE USER albumator;
CREATE SCHEMA albumator AUTHORIZATION albumator;
CREATE DATABASE albumator;
GRANT CONNECT ON DATABASE albumator TO albumator;

-- Start the database server:
--     brew services restart postgresql
--       OR
--     pg_ctl -D /usr/local/var/postgres start
-- Enter a SQL prompt:
--     psql postgres

-- Destroy all tables and rows:
--     TRUNCATE edit, album_order, photo, album, account RESTART IDENTITY CASCADE;
--     DROP TABLE edit_contributor, photo_contributor, album_access, album_order, edit, photo, album, account CASCADE;
--     DROP TYPE permission, contributor;

CREATE TYPE permission AS ENUM ('none', 'read', 'write', 'delete');

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

-- only the photo's owner can modify or delete it
-- related accounts are associated via the photo_contributors table
CREATE TABLE IF NOT EXISTS photo (
    photo_id SERIAL PRIMARY KEY,
    owner_id INTEGER NOT NULL REFERENCES account ON UPDATE CASCADE ON DELETE CASCADE,
    photo_name TEXT NOT NULL,
    photo_desc TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT now(),
    edited_at TIMESTAMP NOT NULL DEFAULT now(),
    file_preview TEXT UNIQUE NOT NULL, -- full resolution HEIC file
    file_source TEXT UNIQUE NOT NULL -- RAW, CR2, TIFF, JPG, etc
);

-- track contributors for each photo, sorted by priority (descending)
CREATE TABLE IF NOT EXISTS photo_contributor (
    account_id INTEGER NOT NULL REFERENCES account ON UPDATE CASCADE ON DELETE CASCADE,
    photo_id INTEGER NOT NULL REFERENCES photo ON UPDATE CASCADE ON DELETE CASCADE,
    contributor CONTRIBUTOR NOT NULL DEFAULT 'other',
    priority INTEGER NOT NULL DEFAULT 0,
    PRIMARY KEY (account_id, photo_id)
);

-- only the edit's owner can modify or delete it
-- related accounts are associated via the edit_contributors table
-- each edit can only be associated with one photo
CREATE TABLE IF NOT EXISTS edit (
    edit_id SERIAL PRIMARY KEY,
    photo_id INTEGER NOT NULL REFERENCES photo ON UPDATE CASCADE ON DELETE CASCADE,
    owner_id INTEGER NOT NULL REFERENCES account ON UPDATE CASCADE ON DELETE CASCADE,
    edit_name TEXT,
    edit_desc TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT now(),
    edited_at TIMESTAMP NOT NULL DEFAULT now(),
    file_preview TEXT UNIQUE NOT NULL, -- full resolution HEIC file
    file_source TEXT UNIQUE NOT NULL, -- XML, JSON, YAML, PSD, etc
    editing_application TEXT NOT NULL -- e.g. Lightroom, Darktable, Photoshop, etc
);

-- track contributors for each edit, sorted by priority (descending)
CREATE TABLE IF NOT EXISTS edit_contributor (
    account_id INTEGER NOT NULL REFERENCES account ON UPDATE CASCADE ON DELETE CASCADE,
    edit_id INTEGER NOT NULL REFERENCES edit ON UPDATE CASCADE ON DELETE CASCADE,
    contributor CONTRIBUTOR NOT NULL DEFAULT 'other',
    priority INTEGER NOT NULL DEFAULT 0,
    PRIMARY KEY (account_id, edit_id)
);

-- only the album's owner can delete it
-- other accounts can modify an album via permissions marked in the album_access table
-- albums contain edits via the album_order table
CREATE TABLE IF NOT EXISTS album (
    album_id SERIAL PRIMARY KEY,
    owner_id INTEGER NOT NULL REFERENCES account ON UPDATE CASCADE ON DELETE CASCADE,
    album_name TEXT NOT NULL,
    album_desc TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT now(),
    edited_at TIMESTAMP NOT NULL DEFAULT now()
);

-- track account permissions for modifying the contents of each album
CREATE TABLE IF NOT EXISTS album_access (
    account_id INTEGER NOT NULL REFERENCES account ON UPDATE CASCADE ON DELETE CASCADE,
    album_id INTEGER NOT NULL REFERENCES album ON UPDATE CASCADE ON DELETE CASCADE,
    permission PERMISSION NOT NULL DEFAULT 'none',
    PRIMARY KEY (account_id, album_id)
);

-- track which albums each edit belongs to, sorted by priority (descending)
CREATE TABLE IF NOT EXISTS album_order (
    album_id INTEGER NOT NULL REFERENCES album ON UPDATE CASCADE ON DELETE CASCADE,
    edit_id INTEGER NOT NULL REFERENCES edit ON UPDATE CASCADE ON DELETE CASCADE,
    priority INTEGER NOT NULL DEFAULT 0,
    PRIMARY KEY (album_id, edit_id)
);

-- insert accounts
INSERT INTO account (account_name) VALUES ('jojo'), ('chumpy'), ('tarzan');

-- insert albums
INSERT INTO album (album_name, album_desc, owner_id)
VALUES ('Landscapes', 'Photos of mountains mostly', 1),
       ('Unorganized', 'Random photos without broader categories', 2);

-- grant accounts access to albums
INSERT INTO album_access (album_id, account_id, permission)
VALUES (1, 1, 'delete'),
       (1, 2, 'read'),
       (1, 3, 'read'),
       (2, 1, 'write'),
       (2, 2, 'delete');

-- insert photos
INSERT INTO photo (
    photo_name,
    owner_id,
    file_preview,
    file_source
) VALUES (
    'mount haruna',
    (SELECT DISTINCT account_id FROM account WHERE account_name = 'jojo'),
    '/path/to/preview.jpg',
    '/path/to/some/file.raw'
), (
    'neander valley',
    (SELECT DISTINCT account_id FROM account WHERE account_name = 'chumpy'),
    '/path/to/another-preview.jpg',
    '/path/to/some/another-file.raw'
);

-- associate contributors with photos
INSERT INTO photo_contributor (photo_id, account_id, contributor)
VALUES (1, 1, 'director'),
       (1, 2, 'photographer'),
       (2, 2, 'photographer'),
       (2, 3, 'editor');

-- insert edits
INSERT INTO edit (
    photo_id,
    owner_id,
    edit_name,
    file_preview,
    file_source
) VALUES (
    1,
    1,
    'My edit',
    '/path/to/preview.jpg',
    '/path/to/some/file.xml'
);

-- associate contributors with edits
INSERT INTO edit_contributor (edit_id, account_id, contributor)
VALUES (1, 1, 'editor'),
       (1, 2, 'assistant');

-- add edits to albums
INSERT INTO album_order (edit_id, album_id, priority)
VALUES (1, (SELECT album_id FROM album WHERE album_name = 'Landscapes' LIMIT 1), 2);

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

-- grab all edits for an album, sorted by priority
SELECT e.edit_id, e.edit_name, album_order.priority FROM album_order
JOIN edit ON album_order.edit_id = edit.edit_id AND album_order.album_id = 1
ORDER BY priority DESC;

-- grab all editors for an album
SELECT account_id, account_name, permission FROM (
    SELECT a.account_id, a.account_name, a.deleted_at, a_a.permission FROM album_access AS a_a
    JOIN account AS a ON a_a.account_id = a.account_id
    WHERE a.deleted_at IS NULL
    AND a_a.album_id = (SELECT album_id FROM album LIMIT 1)
    AND a_a.permission >= 'write'
) AS accounts WHERE deleted_at IS NULL;

-- grab all contributors for a photo
SELECT account_id, account_name, contributor FROM (
    SELECT a.account_id, a.account_name, a.deleted_at, a_p.contributor, a_p.priority
    FROM photo_contributor AS a_p
    JOIN account AS a ON a_p.account_id = a.account_id
    WHERE a.deleted_at IS NULL
    AND a_p.photo_id = (SELECT photo_id FROM photo LIMIT 1)
) AS accounts WHERE deleted_at IS NULL
ORDER BY priority DESC;

-- grab all contributors for an edit
SELECT account_id, account_name, contributor FROM (
    SELECT a.account_id, a.account_name, a.deleted_at, a_e.contributor FROM edit_contributor AS a_e
    JOIN account AS a ON a_e.account_id = a.account_id
    WHERE a.deleted_at IS NULL
    AND a_e.edit_id = (SELECT edit_id FROM edit LIMIT 1)
) AS accounts WHERE deleted_at IS NULL;

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
