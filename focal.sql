CREATE USER focal;
CREATE SCHEMA focal AUTHORIZATION focal;
CREATE DATABASE focal;
GRANT CONNECT ON DATABASE focal TO focal;

-- Destroy all tables and rows:
--     TRUNCATE account, post, reply, raw, edit, manufacturer, camera, lens,
--         editor, preview RESTART IDENTITY CASCADE;
--     DROP TABLE account, post, reply, raw, edit, manufacturer, camera, lens,
--         editor, preview;
--     DROP TYPE account_role, platform;

CREATE TYPE account_role AS ENUM ('user', 'admin');

CREATE TABLE IF NOT EXISTS account (
    account_id   SERIAL PRIMARY KEY,
    account_name VARCHAR(32) UNIQUE NOT NULL,
    account_role ACCOUNT_ROLE NOT NULL DEFAULT 'user',
    created_at   TIMESTAMP NOT NULL DEFAULT now(),
    deleted_at   TIMESTAMP
);

-- Users create a post by:
--     * adding a title (required) and description (optional)
--     * attaching a source image file (required)
--     * attaching an edit source file (optional)
-- For each source image and edit file:
--     * user must attach a preview image
-- Users edit a post by:
--     * changing the title or text
--     * replacing or removing an edit file and its preview image
--     * replacing the source image file
--     * deleting the post
-- Restrict deleting raw images while they're referenced by a post
CREATE TABLE IF NOT EXISTS post (
    post_id    SERIAL PRIMARY KEY,
    account_id INTEGER NOT NULL REFERENCES account ON UPDATE CASCADE ON DELETE CASCADE,
    raw_id     INTEGER NOT NULL REFERENCES raw ON UPDATE CASCADE ON DELETE RESTRICT,
    edit_id    INTEGER REFERENCES edit ON UPDATE CASCADE ON DELETE SET NULL,
    post_title VARCHAR(100) NOT NULL,
    post_text  VARCHAR(1500),
    created_at TIMESTAMP NOT NULL DEFAULT now(),
    edited_at  TIMESTAMP
);

-- Users reply to posts by:
--     * writing a comment and/or attaching an edit
-- For each edit file:
--     * user must attach a preview image
-- Users edit a reply by:
--     * changing the text
--     * replacing or removing an edit file and its preview image
--     * deleting the reply
-- Retain replies (only visible to the logged-in user) after deleting its parent post
-- Restrict deleting edits while they're referenced by a reply
CREATE TABLE IF NOT EXISTS reply (
    reply_id   SERIAL PRIMARY KEY,
    account_id INTEGER NOT NULL REFERENCES account ON UPDATE CASCADE ON DELETE CASCADE,
    post_id    INTEGER REFERENCES post ON UPDATE CASCADE ON DELETE SET NULL,
    edit_id    INTEGER REFERENCES edit ON UPDATE CASCADE ON DELETE RESTRICT,
    reply_text VARCHAR(500),
    created_at TIMESTAMP NOT NULL DEFAULT now(),
    edited_at  TIMESTAMP
);

-- Each raw image is uploaded when a user creates a post
-- Raw images can only be associated with one post
-- For each raw image:
--     * user must attach a preview image
--     * user may specify camera make, model and lens
--     * user may specify metadata, e.g.: aperture, flash, ISO, etc
-- Restrict deleting previews, cameras and lenses while they're referenced by a raw
CREATE TABLE IF NOT EXISTS raw (
    raw_id            SERIAL PRIMARY KEY,
    post_id           INTEGER NOT NULL REFERENCES post ON UPDATE CASCADE ON DELETE CASCADE,
    preview_id        INTEGER NOT NULL REFERENCES preview ON UPDATE CASCADE ON DELETE RESTRICT,
    camera_id         INTEGER REFERENCES camera ON UPDATE CASCADE ON DELETE RESTRICT,
    lens_id           INTEGER REFERENCES lens ON UPDATE CASCADE ON DELETE RESTRICT,
    file_name         VARCHAR(100), -- upload filename preserved to ease back-referencing for users
    file_extension    VARCHAR(20),
    file_path         TEXT UNIQUE NOT NULL, -- server path to source file
    file_size         INTEGER,
    aperture          FLOAT,
    flash             BOOLEAN DEFAULT FALSE,
    focal_length      FLOAT,
    iso               INTEGER,
    shutter_speed_den INTEGER,
    shutter_speed_num INTEGER,
    width             INTEGER,
    height            INTEGER
);

-- Users add edits by:
--     * attaching an edit file to a post or reply
-- For each edit:
--     * user must attach a preview image
--     * user may specify a title and editing software
-- Restrict deleting previews and editors while they're referenced by an edit
CREATE TABLE IF NOT EXISTS edit (
    edit_id        SERIAL PRIMARY KEY,
    post_id        INTEGER REFERENCES post ON UPDATE CASCADE ON DELETE CASCADE,
    reply_id       INTEGER REFERENCES reply ON UPDATE CASCADE ON DELETE CASCADE,
    preview_id     INTEGER NOT NULL REFERENCES preview ON UPDATE CASCADE ON DELETE RESTRICT,
    editor_id      INTEGER REFERENCES editor ON UPDATE CASCADE ON DELETE RESTRICT,
    edit_title     VARCHAR(100),
    file_name      VARCHAR(100), -- upload filename preserved to ease back-referencing for users
    file_extension VARCHAR(20),
    file_path      TEXT UNIQUE NOT NULL, -- server path to source file
    file_size      INTEGER,
    width          INTEGER,
    height         INTEGER,
    CONSTRAINT     post_or_reply CHECK (post_id IS NULL <> reply_id IS NULL) -- require post_id XOR reply_id
);

-- Users add manufacturers by:
--     * specifying a camera or lens for a raw image
CREATE TABLE IF NOT EXISTS manufacturer (
    manufacturer_id   SERIAL PRIMARY KEY,
    manufacturer_name VARCHAR(100) UNIQUE NOT NULL
);

-- Users add cameras by:
--     * specifying the camera make and model for a raw image
-- Restrict deleting manufacturers while they're referenced by a camera
CREATE TABLE IF NOT EXISTS camera (
    camera_id       SERIAL PRIMARY KEY,
    manufacturer_id INTEGER NOT NULL REFERENCES manufacturer ON UPDATE CASCADE ON DELETE RESTRICT,
    camera_model    VARCHAR(100) UNIQUE NOT NULL
);

-- Users add lenses by:
--     * specifying the lens make, model, aperture range and/or focal length for a raw image
-- Restrict deleting manufacturers while they're referenced by a lens
CREATE TABLE IF NOT EXISTS lens (
    lens_id          SERIAL PRIMARY KEY,
    manufacturer_id  INTEGER NOT NULL REFERENCES manufacturer ON UPDATE CASCADE ON DELETE RESTRICT,
    lens_model       VARCHAR(100) UNIQUE NOT NULL,
    aperture_min     FLOAT,
    aperture_max     FLOAT,
    focal_length_min FLOAT,
    focal_length_max FLOAT
);

CREATE TYPE platform AS ENUM ('macOS', 'Windows', 'Linux', 'iOS', 'Android');

-- Users add editors (editing software) by:
--     * attaching an edit to a post or reply
CREATE TABLE IF NOT EXISTS editor (
    editor_id       SERIAL PRIMARY KEY,
    editor_name     VARCHAR(100) NOT NULL,
    editor_version  VARCHAR(20),
    editor_platform PLATFORM
);

-- Preview files are:
--    * uploaded by users
--    * automatically converted to HEIC on upload
--    * resized and converted to JPG when served
CREATE TABLE IF NOT EXISTS preview (
    preview_id SERIAL PRIMARY KEY,
    file_path  TEXT UNIQUE NOT NULL, -- server path to source file
    width      INTEGER NOT NULL,
    height     INTEGER NOT NULL
);
