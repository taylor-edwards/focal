-- CREATE USER focal;
-- CREATE SCHEMA focal AUTHORIZATION focal;
-- CREATE DATABASE focal;
-- GRANT CONNECT ON DATABASE focal TO focal;

-- Destroy all tables and rows:
TRUNCATE account, follow, manufacturer, camera, lens, editor, preview,
photo, edit, reply, tag, photo_tag, upvote, notification, flag RESTART IDENTITY CASCADE;
DROP TABLE account, follow, manufacturer, camera, lens, editor, preview,
photo, edit, reply, tag, photo_tag, upvote, notification, flag;
DROP TYPE account_role, flag_reason, platform, notify_reason, read_status;

CREATE TYPE account_role AS ENUM ('admin', 'user');

CREATE TYPE flag_reason AS ENUM (
    'irrelevant',
    'inappropriate',
    'harmful',
    'impersonation',
    'plagiarism',
    'other'
);

-- Users can register and immediately start following accounts and upvoting
--   content, but can't post or reply until they verify their email.
-- Bans have a set duration which is multiplied by the total number of times
--   they have been banned.
-- Users that are banned more than X times will be permanently banned, which
--   is represented by the account having a valid timestamp for banned_at and
--   NULL for the banned_until column.
CREATE TABLE IF NOT EXISTS account (
    account_id     SERIAL PRIMARY KEY,
    account_role   ACCOUNT_ROLE NOT NULL DEFAULT 'user',
    account_name   VARCHAR(32) UNIQUE NOT NULL,
    email          VARCHAR(200) UNIQUE NOT NULL,
    email_verified BOOLEAN DEFAULT FALSE,
    created_at     TIMESTAMP NOT NULL DEFAULT now(),
    edited_at      TIMESTAMP CHECK (edited_at > created_at),
    deleted_at     TIMESTAMP,
    banned_at      TIMESTAMP,
    banned_until   TIMESTAMP,
    ban_count      INTEGER NOT NULL DEFAULT 0,
    ban_reason     FLAG_REASON
);

-- Users can follow each other to customize the feed shown to them on the homepage.
-- Users that are not logged in or do not follow anyone will be shown the global feed.
-- Followers and following lists are private. Only logged in users can see which accounts
-- they follow. Follower lists are not shown to anyone, but follower count is.
CREATE TABLE IF NOT EXISTS follow (
    follower_id  INTEGER NOT NULL REFERENCES account ON UPDATE CASCADE ON DELETE CASCADE,
    following_id INTEGER NOT NULL REFERENCES account ON UPDATE CASCADE ON DELETE CASCADE,
    PRIMARY KEY (follower_id, following_id)
);

-- Manufacturers of camera and lens equipment.
CREATE TABLE IF NOT EXISTS manufacturer (
    manufacturer_id   SERIAL PRIMARY KEY,
    manufacturer_name VARCHAR(100) UNIQUE NOT NULL
);

-- Cameras referenced by photo submissions.
CREATE TABLE IF NOT EXISTS camera (
    camera_id       SERIAL PRIMARY KEY,
    manufacturer_id INTEGER NOT NULL REFERENCES manufacturer ON UPDATE CASCADE ON DELETE RESTRICT,
    camera_model    VARCHAR(100) NOT NULL,
    UNIQUE (camera_model, manufacturer_id)
);

-- Lenses referenced by photo submissions.
CREATE TABLE IF NOT EXISTS lens (
    lens_id          SERIAL PRIMARY KEY,
    manufacturer_id  INTEGER NOT NULL REFERENCES manufacturer ON UPDATE CASCADE ON DELETE RESTRICT,
    lens_model       VARCHAR(100) NOT NULL,
    aperture_min     FLOAT CHECK (aperture_min > 0),
    aperture_max     FLOAT CHECK (aperture_max > 0),
    focal_length_min FLOAT CHECK (focal_length_min > 0),
    focal_length_max FLOAT CHECK (focal_length_max > 0),
    UNIQUE (lens_model, manufacturer_id)
);

CREATE TYPE platform AS ENUM (
    'Android',
    'iOS',
    'Linux',
    'macOS',
    'Windows'
);

-- Editing software referenced by edit submissions.
CREATE TABLE IF NOT EXISTS editor (
    editor_id       SERIAL PRIMARY KEY,
    editor_name     VARCHAR(100) NOT NULL,
    editor_version  VARCHAR(20),
    editor_platform PLATFORM,
    UNIQUE (editor_name, editor_version, editor_platform)
);

-- Previews can be submitted by users or automatically generated
-- from raw files. They are always stored in HEIC format and are
-- converted and resized when being served to the client.
CREATE TABLE IF NOT EXISTS preview (
    preview_id        SERIAL PRIMARY KEY,
    preview_file_path TEXT UNIQUE NOT NULL,
    preview_file_size INTEGER NOT NULL CHECK (preview_file_size > 0),
    preview_width     INTEGER NOT NULL CHECK (preview_width > 0),
    preview_height    INTEGER NOT NULL CHECK (preview_height > 0)
);

-- Photos are the top-level submission type. Users are encouraged to
-- include the original raw file but any image format is accepted to
-- support the widest range of user inputs.
CREATE TABLE IF NOT EXISTS photo (
    photo_id           SERIAL PRIMARY KEY,
    account_id         INTEGER NOT NULL REFERENCES account ON UPDATE CASCADE ON DELETE CASCADE,
    preview_id         INTEGER NOT NULL REFERENCES preview ON UPDATE CASCADE ON DELETE RESTRICT,
    camera_id          INTEGER REFERENCES camera ON UPDATE CASCADE ON DELETE RESTRICT,
    lens_id            INTEGER REFERENCES lens ON UPDATE CASCADE ON DELETE RESTRICT,
    photo_title        VARCHAR(100),
    photo_description  VARCHAR(2500),
    raw_file_path      TEXT UNIQUE NOT NULL,
    raw_file_extension VARCHAR(32) NOT NULL,
    raw_file_size      INTEGER NOT NULL CHECK (raw_file_size > 0),
    raw_width          INTEGER CHECK (raw_width > 0),
    raw_height         INTEGER CHECK (raw_height > 0),
    aperture           FLOAT CHECK (aperture > 0),
    flash              BOOLEAN DEFAULT FALSE,
    focal_length       FLOAT CHECK (focal_length > 0),
    iso                INTEGER CHECK (iso > 0),
    shutter_speed_den  INTEGER CHECK (shutter_speed_den > 0),
    shutter_speed_num  INTEGER CHECK (shutter_speed_num > 0),
    created_at         TIMESTAMP NOT NULL DEFAULT now(),
    edited_at          TIMESTAMP CHECK (edited_at > created_at),
    CONSTRAINT title_or_desc CHECK (photo_title IS NOT NULL OR photo_description IS NOT NULL)
);

-- Edits are essentially forks of a (raw) photo. Users must upload their own
-- preview image (not all editing software can be ran server-side) and they
-- are encouraged to upload a sidecar file if their editor can export one.
CREATE TABLE IF NOT EXISTS edit (
    edit_id             SERIAL PRIMARY KEY,
    account_id          INTEGER NOT NULL REFERENCES account ON UPDATE CASCADE ON DELETE CASCADE,
    preview_id          INTEGER NOT NULL REFERENCES preview ON UPDATE CASCADE ON DELETE RESTRICT,
    photo_id            INTEGER REFERENCES photo ON UPDATE CASCADE ON DELETE SET NULL,
    editor_id           INTEGER REFERENCES editor ON UPDATE CASCADE ON DELETE RESTRICT,
    edit_title          VARCHAR(100),
    edit_description    VARCHAR(2500),
    edit_file_path      TEXT UNIQUE,
    edit_file_extension VARCHAR(32),
    edit_file_size      INTEGER CHECK (edit_file_size > 0),
    edit_width          INTEGER CHECK (edit_width > 0),
    edit_height         INTEGER CHECK (edit_height > 0),
    created_at          TIMESTAMP NOT NULL DEFAULT now(),
    edited_at           TIMESTAMP CHECK (edited_at > created_at),
    CONSTRAINT title_or_desc CHECK (edit_title IS NOT NULL OR edit_description IS NOT NULL)
);

-- Users can reply in text to photos and edits.
CREATE TABLE IF NOT EXISTS reply (
    reply_id   SERIAL PRIMARY KEY,
    account_id INTEGER NOT NULL REFERENCES account ON UPDATE CASCADE ON DELETE CASCADE,
    photo_id   INTEGER REFERENCES photo ON UPDATE CASCADE ON DELETE CASCADE,
    edit_id    INTEGER REFERENCES edit ON UPDATE CASCADE ON DELETE CASCADE,
    reply_text VARCHAR(500),
    created_at TIMESTAMP NOT NULL DEFAULT now(),
    edited_at  TIMESTAMP CHECK (edited_at > created_at),
    CONSTRAINT single_target CHECK ((photo_id IS NULL) <> (edit_id IS NULL)) -- only specify one foreign key
);

-- User generated tags. Currently only applied to photos.
CREATE TABLE IF NOT EXISTS tag (
    tag_id   SERIAL PRIMARY KEY,
    tag_name VARCHAR(32) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS photo_tag (
    photo_id INTEGER NOT NULL REFERENCES photo ON UPDATE CASCADE ON DELETE CASCADE,
    tag_id   INTEGER NOT NULL REFERENCES tag ON UPDATE CASCADE ON DELETE RESTRICT,
    PRIMARY KEY (photo_id, tag_id)
);

-- Users can upvote photos, edits and replies to signal their support.
CREATE TABLE IF NOT EXISTS upvote (
    upvote_id        SERIAL PRIMARY KEY,
    account_id       INTEGER NOT NULL REFERENCES account ON UPDATE CASCADE ON DELETE CASCADE,
    upvoted_photo_id INTEGER REFERENCES photo ON UPDATE CASCADE ON DELETE CASCADE,
    upvoted_edit_id  INTEGER REFERENCES edit ON UPDATE CASCADE ON DELETE CASCADE,
    upvoted_reply_id INTEGER REFERENCES reply ON UPDATE CASCADE ON DELETE CASCADE,
    created_at       TIMESTAMP NOT NULL DEFAULT now(),
    UNIQUE (account_id, upvoted_photo_id, upvoted_edit_id, upvoted_reply_id),
    -- only specify one foreign key
    CHECK ((upvoted_photo_id IS NOT NULL)::INTEGER +
           (upvoted_edit_id  IS NOT NULL)::INTEGER +
           (upvoted_reply_id IS NOT NULL)::INTEGER = 1)
);

CREATE TYPE notify_reason AS ENUM ('replied', 'submitted_edit', 'upvoted');

CREATE TYPE read_status AS ENUM ('unread', 'read');

-- Notify users when others reply to, submit edits to, or upvote one of their posts.
-- Automatically delete notifications that have been read and are >30 days old.
-- Users can manually delete any or all notifications at any time.
CREATE TABLE IF NOT EXISTS notification (
    notification_id   SERIAL PRIMARY KEY,
    recipient_id      INTEGER NOT NULL REFERENCES account ON UPDATE CASCADE ON DELETE CASCADE,
    actor_id          INTEGER NOT NULL REFERENCES account ON UPDATE CASCADE ON DELETE CASCADE,
    target_photo_id   INTEGER REFERENCES photo ON UPDATE CASCADE ON DELETE CASCADE,
    target_edit_id    INTEGER REFERENCES edit ON UPDATE CASCADE ON DELETE CASCADE,
    created_edit_id   INTEGER REFERENCES edit ON UPDATE CASCADE ON DELETE CASCADE,
    created_reply_id  INTEGER REFERENCES reply ON UPDATE CASCADE ON DELETE CASCADE,
    created_upvote_id INTEGER REFERENCES upvote ON UPDATE CASCADE ON DELETE CASCADE,
    notify_reason     NOTIFY_REASON NOT NULL,
    read_status       READ_STATUS NOT NULL DEFAULT 'unread',
    created_at        TIMESTAMP NOT NULL DEFAULT now(),
    -- only specify one foreign key for targeted content
    CONSTRAINT single_target CHECK ((target_photo_id IS NULL) <> (target_edit_id IS NULL)),
    -- only specify one foreign key for generated content / the action taken
    CONSTRAINT single_source CHECK (
        (created_edit_id IS NOT NULL)::INTEGER +
        (created_reply_id IS NOT NULL)::INTEGER +
        (created_upvote_id IS NOT NULL)::INTEGER = 1
    )
);

-- Verified users can flag accounts and content for various reasons. Admins can review
-- flagged content for moderation, including: deletion, banning and notifying the user.
CREATE TABLE IF NOT EXISTS flag (
    flag_id            SERIAL PRIMARY KEY,
    account_id         INTEGER NOT NULL REFERENCES account ON UPDATE CASCADE ON DELETE CASCADE,
    flagged_account_id INTEGER REFERENCES account ON UPDATE CASCADE ON DELETE CASCADE,
    flagged_photo_id   INTEGER REFERENCES photo ON UPDATE CASCADE ON DELETE CASCADE,
    flagged_edit_id    INTEGER REFERENCES edit ON UPDATE CASCADE ON DELETE CASCADE,
    flagged_reply_id   INTEGER REFERENCES reply ON UPDATE CASCADE ON DELETE CASCADE,
    flag_reason        FLAG_REASON NOT NULL,
    reason_text        VARCHAR(500),
    created_at         TIMESTAMP NOT NULL DEFAULT now(),
    UNIQUE (account_id, flagged_account_id, flagged_photo_id, flagged_edit_id, flagged_reply_id),
    -- only specify one foreign key
    CONSTRAINT single_target CHECK (
        (flagged_account_id IS NOT NULL)::INTEGER +
        (flagged_photo_id   IS NOT NULL)::INTEGER +
        (flagged_edit_id    IS NOT NULL)::INTEGER +
        (flagged_reply_id   IS NOT NULL)::INTEGER = 1
    )
);
