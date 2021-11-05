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
--     TRUNCATE account, album, album_access, album_order, album_tag, edit, edit_contributor,
--         edit_tag, photo, photo_contributor, photo_tag, tag RESTART IDENTITY CASCADE;
--     DROP TABLE account, album, album_access, album_order, album_tag, edit, edit_contributor,
--         edit_tag, photo, photo_contributor, photo_tag, tag CASCADE;
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
    account_name VARCHAR(32) UNIQUE NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT now(),
    edited_at TIMESTAMP NOT NULL DEFAULT now(),
    deleted_at TIMESTAMP
);

-- only the photo's owner can modify or delete it
-- related accounts are associated via the photo_contributors table
CREATE TABLE IF NOT EXISTS photo (
    photo_id SERIAL PRIMARY KEY,
    owner_id INTEGER NOT NULL REFERENCES account ON UPDATE CASCADE ON DELETE CASCADE,
    photo_name VARCHAR(32) NOT NULL,
    photo_desc TEXT,
    camera VARCHAR(32) NOT NULL, -- e.g. Fujifilm XT-3 15mm 2.8f
    file_preview TEXT UNIQUE NOT NULL, -- full resolution HEIC file
    file_source TEXT UNIQUE NOT NULL, -- RAW, CR2, TIFF, JPG, etc
    created_at TIMESTAMP NOT NULL DEFAULT now(),
    edited_at TIMESTAMP NOT NULL DEFAULT now()
);

-- track contributors for each photo, sorted by priority (descending)
CREATE TABLE IF NOT EXISTS photo_contributor (
    account_id INTEGER NOT NULL REFERENCES account ON UPDATE CASCADE ON DELETE CASCADE,
    photo_id INTEGER NOT NULL REFERENCES photo ON UPDATE CASCADE ON DELETE CASCADE,
    contributor CONTRIBUTOR NOT NULL DEFAULT 'photographer',
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
    edit_name VARCHAR(32),
    edit_desc TEXT,
    edit_tool VARCHAR(32) NOT NULL, -- e.g. Lightroom, Darktable, Photoshop, etc
    file_preview TEXT UNIQUE NOT NULL, -- full resolution HEIC file
    file_source TEXT UNIQUE NOT NULL, -- XML, JSON, YAML, PSD, etc
    created_at TIMESTAMP NOT NULL DEFAULT now(),
    edited_at TIMESTAMP NOT NULL DEFAULT now()
);

-- track contributors for each edit, sorted by priority (descending)
CREATE TABLE IF NOT EXISTS edit_contributor (
    account_id INTEGER NOT NULL REFERENCES account ON UPDATE CASCADE ON DELETE CASCADE,
    edit_id INTEGER NOT NULL REFERENCES edit ON UPDATE CASCADE ON DELETE CASCADE,
    contributor CONTRIBUTOR NOT NULL DEFAULT 'editor',
    priority INTEGER NOT NULL DEFAULT 0,
    PRIMARY KEY (account_id, edit_id)
);

-- only the album's owner can delete it
-- other accounts can modify an album via permissions marked in the album_access table
-- albums contain edits via the album_order table
CREATE TABLE IF NOT EXISTS album (
    album_id SERIAL PRIMARY KEY,
    owner_id INTEGER NOT NULL REFERENCES account ON UPDATE CASCADE ON DELETE CASCADE,
    album_name VARCHAR(32) NOT NULL,
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

-- track tags on photos, edits and albums
CREATE TABLE IF NOT EXISTS tag (
    tag_id SERIAL PRIMARY KEY,
    tag_name VARCHAR(24) UNIQUE NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS photo_tag (
    tag_id INTEGER NOT NULL REFERENCES tag ON UPDATE CASCADE ON DELETE CASCADE,
    photo_id INTEGER NOT NULL REFERENCES photo ON UPDATE CASCADE ON DELETE CASCADE,
    PRIMARY KEY (tag_id, photo_id)
);

CREATE TABLE IF NOT EXISTS edit_tag (
    tag_id INTEGER NOT NULL REFERENCES tag ON UPDATE CASCADE ON DELETE CASCADE,
    edit_id INTEGER NOT NULL REFERENCES edit ON UPDATE CASCADE ON DELETE CASCADE,
    PRIMARY KEY (tag_id, edit_id)
);

CREATE TABLE IF NOT EXISTS album_tag (
    tag_id INTEGER NOT NULL REFERENCES tag ON UPDATE CASCADE ON DELETE CASCADE,
    album_id INTEGER NOT NULL REFERENCES album ON UPDATE CASCADE ON DELETE CASCADE,
    PRIMARY KEY (tag_id, album_id)
);

-- insert accounts
INSERT INTO account (account_name)
VALUES ('jojo'), ('chumpy'), ('tarzan'), ('alfa'), ('hoodoo');

-- insert albums
INSERT INTO album (album_name, album_desc, owner_id)
VALUES (
    'Landscapes',
    'Photos of mountains mostly',
    (SELECT account_id FROM account WHERE account_name = 'tarzan')
), (
    'Screenshots',
    'In-game captures from Legend of Mana',
    (SELECT account_id FROM account WHERE account_name = 'chumpy')
), (
    'Hawaii',
    'Photos from our trip to Hawaii',
    (SELECT account_id FROM account WHERE account_name = 'chumpy')
);

-- grant accounts access to the contents of albums
INSERT INTO album_access (album_id, account_id, permission)
VALUES (
    (SELECT album_id FROM album WHERE album_name = 'Landscapes' LIMIT 1),
    (SELECT DISTINCT account_id FROM account WHERE account_name = 'tarzan'),
    'delete'
), (
    (SELECT album_id FROM album WHERE album_name = 'Landscapes' LIMIT 1),
    (SELECT DISTINCT account_id FROM account WHERE account_name = 'jojo'),
    'write'
), (
    (SELECT album_id FROM album WHERE album_name = 'Landscapes' LIMIT 1),
    (SELECT DISTINCT account_id FROM account WHERE account_name = 'hoodoo'),
    'read'
), (
    (SELECT album_id FROM album WHERE album_name = 'Screenshots' LIMIT 1),
    (SELECT DISTINCT account_id FROM account WHERE account_name = 'chumpy'),
    'delete'
), (
    (SELECT album_id FROM album WHERE album_name = 'Hawaii' LIMIT 1),
    (SELECT DISTINCT account_id FROM account WHERE account_name = 'alfa'),
    'write'
), (
    (SELECT album_id FROM album WHERE album_name = 'Hawaii' LIMIT 1),
    (SELECT DISTINCT account_id FROM account WHERE account_name = 'hoodoo'),
    'read'
);

-- insert photos
INSERT INTO photo (
    photo_name,
    camera,
    owner_id,
    file_preview,
    file_source
) VALUES (
    'Mount Akina',
    'Canon Rebel T5',
    (SELECT DISTINCT account_id FROM account WHERE account_name = 'tarzan'),
    '/path/to/preview1.heic',
    '/path/to/some/file1.raw'
), (
    'Foggy foothills',
    'Canon Rebel T5',
    (SELECT DISTINCT account_id FROM account WHERE account_name = 'jojo'),
    '/path/to/preview2.heic',
    '/path/to/some/file2.cr2'
), (
    'Double chimney Toadstoolshed',
    'Screenshot',
    (SELECT DISTINCT account_id FROM account WHERE account_name = 'chumpy'),
    '/path/to/preview5.heic',
    '/path/to/some/file5.raf'
), (
    'Ultimate sword',
    'Screenshot',
    (SELECT DISTINCT account_id FROM account WHERE account_name = 'chumpy'),
    '/path/to/preview6.heic',
    '/path/to/some/file6.raf'
), (
    'Hotel view',
    'Fujifilm XT-3',
    (SELECT DISTINCT account_id FROM account WHERE account_name = 'alfa'),
    '/path/to/preview3.heic',
    '/path/to/some/file3.raw'
), (
    'Diamond Head',
    'Fujifilm XT-3',
    (SELECT DISTINCT account_id FROM account WHERE account_name = 'chumpy'),
    '/path/to/preview4.heic',
    '/path/to/some/file4.raf'
), (
    'Nuuanu Pali Lookout',
    'Fujifilm XT-3',
    (SELECT DISTINCT account_id FROM account WHERE account_name = 'alfa'),
    '/path/to/preview7.heic',
    '/path/to/some/file7.cr2'
);

-- associate contributors with photos
INSERT INTO photo_contributor (photo_id, account_id, contributor)
VALUES (
    (SELECT photo_id FROM photo WHERE photo_name = 'Mount Akina' LIMIT 1),
    (SELECT DISTINCT account_id FROM account WHERE account_name = 'tarzan'),
    'photographer'
), (
    (SELECT photo_id FROM photo WHERE photo_name = 'Mount Akina' LIMIT 1),
    (SELECT DISTINCT account_id FROM account WHERE account_name = 'hoodoo'),
    'director'
), (
    (SELECT photo_id FROM photo WHERE photo_name = 'Foggy foothills' LIMIT 1),
    (SELECT DISTINCT account_id FROM account WHERE account_name = 'jojo'),
    'photographer'
), (
    (SELECT photo_id FROM photo WHERE photo_name = 'Double chimney Toadstoolshed' LIMIT 1),
    (SELECT DISTINCT account_id FROM account WHERE account_name = 'chumpy'),
    'photographer'
), (
    (SELECT photo_id FROM photo WHERE photo_name = 'Ultimate sword' LIMIT 1),
    (SELECT DISTINCT account_id FROM account WHERE account_name = 'chumpy'),
    'photographer'
), (
    (SELECT photo_id FROM photo WHERE photo_name = 'Hotel view' LIMIT 1),
    (SELECT DISTINCT account_id FROM account WHERE account_name = 'alfa'),
    'photographer'
), (
    (SELECT photo_id FROM photo WHERE photo_name = 'Diamond Head' LIMIT 1),
    (SELECT DISTINCT account_id FROM account WHERE account_name = 'chumpy'),
    'photographer'
), (
    (SELECT photo_id FROM photo WHERE photo_name = 'Diamond Head' LIMIT 1),
    (SELECT DISTINCT account_id FROM account WHERE account_name = 'hoodoo'),
    'assistant'
), (
    (SELECT photo_id FROM photo WHERE photo_name = 'Nuuanu Pali Lookout' LIMIT 1),
    (SELECT DISTINCT account_id FROM account WHERE account_name = 'alfa'),
    'photographer'
);

-- insert edits
INSERT INTO edit (
    edit_name,
    photo_id,
    owner_id,
    file_preview,
    file_source,
    edit_tool
) VALUES (
    'Dramatic Mount Akina',
    (SELECT photo_id FROM photo WHERE photo_name = 'Mount Akina' LIMIT 1),
    (SELECT DISTINCT account_id FROM account WHERE account_name = 'chumpy'),
    '/path/to/preview1.heic',
    '/path/to/file1.xml',
    'Lightroom'
), (
    'Mountain Fog',
    (SELECT photo_id FROM photo WHERE photo_name = 'Foggy foothills' LIMIT 1),
    (SELECT DISTINCT account_id FROM account WHERE account_name = 'alfa'),
    '/path/to/preview2.heic',
    '/path/to/file2.xml',
    'Photoshop'
), (
    'Nuuanu Pali Lookout wide crop',
    (SELECT photo_id FROM photo WHERE photo_name = 'Nuuanu Pali Lookout' LIMIT 1),
    (SELECT DISTINCT account_id FROM account WHERE account_name = 'hoodoo'),
    '/path/to/preview3.heic',
    '/path/to/file3.xml',
    'Darktable'
), (
    'Hotel view',
    (SELECT photo_id FROM photo WHERE photo_name = 'Hotel view' LIMIT 1),
    (SELECT DISTINCT account_id FROM account WHERE account_name = 'alfa'),
    '/path/to/preview4.heic',
    '/path/to/file4.xml',
    'Darktable'
), (
    'Diamond Head',
    (SELECT photo_id FROM photo WHERE photo_name = 'Diamond Head' LIMIT 1),
    (SELECT DISTINCT account_id FROM account WHERE account_name = 'chumpy'),
    '/path/to/preview5.heic',
    '/path/to/file5.xml',
    'Darktable'
), (
    'Nuuanu Pali Lookout',
    (SELECT photo_id FROM photo WHERE photo_name = 'Nuuanu Pali Lookout' LIMIT 1),
    (SELECT DISTINCT account_id FROM account WHERE account_name = 'alfa'),
    '/path/to/preview6.heic',
    '/path/to/file6.xml',
    'Lightroom'
), (
    'Double chimney Toadstoolshed',
    (SELECT photo_id FROM photo WHERE photo_name = 'Double chimney Toadstoolshed' LIMIT 1),
    (SELECT DISTINCT account_id FROM account WHERE account_name = 'chumpy'),
    '/path/to/preview7.heic',
    '/path/to/file7.xml',
    'Darktable'
), (
    'Ultimate sword',
    (SELECT photo_id FROM photo WHERE photo_name = 'Ultimate sword' LIMIT 1),
    (SELECT DISTINCT account_id FROM account WHERE account_name = 'chumpy'),
    '/path/to/preview8.heic',
    '/path/to/file8.xml',
    'Darktable'
), (
    'Mount Akina',
    (SELECT photo_id FROM photo WHERE photo_name = 'Mount Akina' LIMIT 1),
    (SELECT DISTINCT account_id FROM account WHERE account_name = 'tarzan'),
    '/path/to/preview9.heic',
    '/path/to/file9.xml',
    'Lightroom'
);

-- associate contributors with edits
INSERT INTO edit_contributor (contributor, edit_id, account_id)
VALUES (
    'editor',
    (SELECT edit_id FROM edit WHERE edit_name = 'Dramatic Mount Akina' LIMIT 1),
    (SELECT DISTINCT account_id FROM account WHERE account_name = 'chumpy')
), (
    'editor',
    (SELECT edit_id FROM edit WHERE edit_name = 'Mountain Fog' LIMIT 1),
    (SELECT DISTINCT account_id FROM account WHERE account_name = 'alfa')
), (
    'editor',
    (SELECT edit_id FROM edit WHERE edit_name = 'Nuuanu Pali Lookout wide crop' LIMIT 1),
    (SELECT DISTINCT account_id FROM account WHERE account_name = 'hoodoo')
), (
    'editor',
    (SELECT edit_id FROM edit WHERE edit_name = 'Hotel view' LIMIT 1),
    (SELECT DISTINCT account_id FROM account WHERE account_name = 'alfa')
), (
    'editor',
    (SELECT edit_id FROM edit WHERE edit_name = 'Diamond Head' LIMIT 1),
    (SELECT DISTINCT account_id FROM account WHERE account_name = 'chumpy')
), (
    'editor',
    (SELECT edit_id FROM edit WHERE edit_name = 'Nuuanu Pali Lookout' LIMIT 1),
    (SELECT DISTINCT account_id FROM account WHERE account_name = 'alfa')
), (
    'editor',
    (SELECT edit_id FROM edit WHERE edit_name = 'Double chimney Toadstoolshed' LIMIT 1),
    (SELECT DISTINCT account_id FROM account WHERE account_name = 'chumpy')
), (
    'editor',
    (SELECT edit_id FROM edit WHERE edit_name = 'Ultimate sword' LIMIT 1),
    (SELECT DISTINCT account_id FROM account WHERE account_name = 'chumpy')
), (
    'editor',
    (SELECT edit_id FROM edit WHERE edit_name = 'Mount Akina' LIMIT 1),
    (SELECT DISTINCT account_id FROM account WHERE account_name = 'tarzan')
);

-- add edits to albums
INSERT INTO album_order (album_id, edit_id, priority)
VALUES (
    (SELECT album_id FROM album WHERE album_name = 'Landscapes' LIMIT 1),
    (SELECT edit_id FROM edit WHERE edit_name = 'Dramatic Mount Akina' LIMIT 1),
    6
), (
    (SELECT album_id FROM album WHERE album_name = 'Landscapes' LIMIT 1),
    (SELECT edit_id FROM edit WHERE edit_name = 'Mount Akina' LIMIT 1),
    5
), (
    (SELECT album_id FROM album WHERE album_name = 'Landscapes' LIMIT 1),
    (SELECT edit_id FROM edit WHERE edit_name = 'Mountain Fog' LIMIT 1),
    4
), (
    (SELECT album_id FROM album WHERE album_name = 'Landscapes' LIMIT 1),
    (SELECT edit_id FROM edit WHERE edit_name = 'Nuuanu Pali Lookout wide crop' LIMIT 1),
    3
), (
    (SELECT album_id FROM album WHERE album_name = 'Landscapes' LIMIT 1),
    (SELECT edit_id FROM edit WHERE edit_name = 'Diamond Head' LIMIT 1),
    2
), (
    (SELECT album_id FROM album WHERE album_name = 'Landscapes' LIMIT 1),
    (SELECT edit_id FROM edit WHERE edit_name = 'Nuuanu Pali Lookout' LIMIT 1),
    1
), (
    (SELECT album_id FROM album WHERE album_name = 'Hawaii' LIMIT 1),
    (SELECT edit_id FROM edit WHERE edit_name = 'Nuuanu Pali Lookout wide crop' LIMIT 1),
    4
), (
    (SELECT album_id FROM album WHERE album_name = 'Hawaii' LIMIT 1),
    (SELECT edit_id FROM edit WHERE edit_name = 'Nuuanu Pali Lookout' LIMIT 1),
    3
), (
    (SELECT album_id FROM album WHERE album_name = 'Hawaii' LIMIT 1),
    (SELECT edit_id FROM edit WHERE edit_name = 'Diamond Head' LIMIT 1),
    2
), (
    (SELECT album_id FROM album WHERE album_name = 'Hawaii' LIMIT 1),
    (SELECT edit_id FROM edit WHERE edit_name = 'Hotel view' LIMIT 1),
    1
), (
    (SELECT album_id FROM album WHERE album_name = 'Screenshots' LIMIT 1),
    (SELECT edit_id FROM edit WHERE edit_name = 'Double chimney Toadstoolshed' LIMIT 1),
    0
), (
    (SELECT album_id FROM album WHERE album_name = 'Screenshots' LIMIT 1),
    (SELECT edit_id FROM edit WHERE edit_name = 'Ultimate sword' LIMIT 1),
    0
);

-- create tags
INSERT INTO tag (tag_name)
VALUES ('canon'), ('nikon'), ('gaming'), ('tropical'), ('dark'), ('light');

-- apply tags to photos
INSERT INTO photo_tag (photo_id, tag_id)
VALUES (
    (SELECT photo_id FROM photo WHERE photo_name = 'Mount Akina' LIMIT 1),
    (SELECT tag_id FROM tag WHERE tag_name = 'nikon')
),(
    (SELECT photo_id FROM photo WHERE photo_name = 'Foggy foothills' LIMIT 1),
    (SELECT tag_id FROM tag WHERE tag_name = 'nikon')
),(
    (SELECT photo_id FROM photo WHERE photo_name = 'Double chimney Toadstoolshed' LIMIT 1),
    (SELECT tag_id FROM tag WHERE tag_name = 'gaming')
), (
    (SELECT photo_id FROM photo WHERE photo_name = 'Ultimate sword' LIMIT 1),
    (SELECT tag_id FROM tag WHERE tag_name = 'gaming')
), (
    (SELECT photo_id FROM photo WHERE photo_name = 'Diamond Head' LIMIT 1),
    (SELECT tag_id FROM tag WHERE tag_name = 'canon')
), (
    (SELECT photo_id FROM photo WHERE photo_name = 'Diamond Head' LIMIT 1),
    (SELECT tag_id FROM tag WHERE tag_name = 'tropical')
), (
    (SELECT photo_id FROM photo WHERE photo_name = 'Nuuanu Pali Lookout' LIMIT 1),
    (SELECT tag_id FROM tag WHERE tag_name = 'canon')
), (
    (SELECT photo_id FROM photo WHERE photo_name = 'Nuuanu Pali Lookout' LIMIT 1),
    (SELECT tag_id FROM tag WHERE tag_name = 'tropical')
);

-- apply tags to edits
INSERT INTO edit_tag (edit_id, tag_id)
VALUES (
    (SELECT edit_id FROM edit WHERE edit_name = 'Mount Akina' LIMIT 1),
    (SELECT tag_id FROM tag WHERE tag_name = 'light')
), (
    (SELECT edit_id FROM edit WHERE edit_name = 'Dramatic Mount Akina' LIMIT 1),
    (SELECT tag_id FROM tag WHERE tag_name = 'dark')
),(
    (SELECT edit_id FROM edit WHERE edit_name = 'Double chimney Toadstoolshed' LIMIT 1),
    (SELECT tag_id FROM tag WHERE tag_name = 'gaming')
), (
    (SELECT edit_id FROM edit WHERE edit_name = 'Ultimate sword' LIMIT 1),
    (SELECT tag_id FROM tag WHERE tag_name = 'gaming')
), (
    (SELECT edit_id FROM edit WHERE edit_name = 'Diamond Head' LIMIT 1),
    (SELECT tag_id FROM tag WHERE tag_name = 'canon')
), (
    (SELECT edit_id FROM edit WHERE edit_name = 'Nuuanu Pali Lookout' LIMIT 1),
    (SELECT tag_id FROM tag WHERE tag_name = 'canon')
), (
    (SELECT edit_id FROM edit WHERE edit_name = 'Diamond Head' LIMIT 1),
    (SELECT tag_id FROM tag WHERE tag_name = 'tropical')
), (
    (SELECT edit_id FROM edit WHERE edit_name = 'Nuuanu Pali Lookout' LIMIT 1),
    (SELECT tag_id FROM tag WHERE tag_name = 'tropical')
);

-- apply tags to albums
INSERT INTO album_tag (album_id, tag_id)
VALUES (
    (SELECT album_id FROM album WHERE album_name = 'Landscapes' LIMIT 1),
    (SELECT tag_id FROM tag WHERE tag_name = 'nikon')
), (
    (SELECT album_id FROM album WHERE album_name = 'Screenshots' LIMIT 1),
    (SELECT tag_id FROM tag WHERE tag_name = 'gaming')
), (
    (SELECT album_id FROM album WHERE album_name = 'Hawaii' LIMIT 1),
    (SELECT tag_id FROM tag WHERE tag_name = 'tropical')
), (
    (SELECT album_id FROM album WHERE album_name = 'Hawaii' LIMIT 1),
    (SELECT tag_id FROM tag WHERE tag_name = 'canon')
);

-- grab all accounts
SELECT account_id, account_name, created_at FROM account WHERE deleted_at IS NULL;

-- grab all albums for an account
SELECT a.album_id, a.album_name, a.album_desc, a.created_at, a.edited_at, a_a.permission
FROM album_access AS a_a
JOIN album AS a ON a_a.album_id = a.album_id
WHERE a_a.account_id = (
    SELECT account_id FROM account WHERE deleted_at IS NULL OFFSET 4 LIMIT 1
);

-- grab all photos for an account
SELECT p.photo_id, p.photo_name, p.photo_desc, p.created_at, p.edited_at, p_c.contributor
FROM photo_contributor AS p_c
JOIN photo AS p ON p_c.photo_id = p.photo_id
WHERE p_c.account_id = (
    SELECT account_id FROM account WHERE deleted_at IS NULL OFFSET 3 LIMIT 1
);

-- grab all edits for an account
SELECT e.edit_id, e.edit_name, e.edit_desc, e.created_at, e.edited_at, e_c.contributor
FROM edit_contributor AS e_c
JOIN edit AS e ON e_c.edit_id = e.edit_id
WHERE e_c.account_id = (
    SELECT account_id FROM account WHERE deleted_at IS NULL OFFSET 1 LIMIT 1
);

-- grab all edits for an album, sorted by priority
SELECT e.edit_id, e.edit_name, a_o.priority FROM album_order AS a_o
JOIN edit AS e ON a_o.edit_id = e.edit_id AND a_o.album_id = 1
ORDER BY priority DESC;

-- grab all editors for an album
SELECT account_id, account_name, permission FROM (
    SELECT a.account_id, a.account_name, a.deleted_at, a_a.permission
    FROM album_access AS a_a
    JOIN account AS a ON a_a.account_id = a.account_id
    WHERE a.deleted_at IS NULL
    AND a_a.album_id = (SELECT album_id FROM album LIMIT 1)
    AND a_a.permission >= 'write'
) AS accounts WHERE deleted_at IS NULL;

-- grab all contributors for a photo
SELECT account_id, account_name, contributor FROM (
    SELECT a.account_id, a.account_name, a.deleted_at, p_c.contributor, p_c.priority
    FROM photo_contributor AS p_c
    JOIN account AS a ON p_c.account_id = a.account_id
    WHERE a.deleted_at IS NULL
    AND p_c.photo_id = (SELECT photo_id FROM photo LIMIT 1)
) AS accounts WHERE deleted_at IS NULL
ORDER BY priority DESC;

-- grab all contributors for an edit
SELECT account_id, account_name, contributor FROM (
    SELECT a.account_id, a.account_name, a.deleted_at, e_c.contributor
    FROM edit_contributor AS e_c
    JOIN account AS a ON e_c.account_id = a.account_id
    WHERE a.deleted_at IS NULL
    AND e_c.edit_id = (SELECT edit_id FROM edit LIMIT 1)
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
