# Focal Web

The web client uses NextJS to pre-render and serve publicly accessible
templates and APIs.

The app's public pages are:

```
+----------------------------+-----------------------------+
| PUBLIC PATH                | USER FACING CONTENT         |
+----------------------------+-----------------------------+
| /                          | Home page                   |
| /a                         | Login page                  |
| /l                         | Logout page                 |
| /p                         | Photo feed                  |
| /e                         | Edit feed                   |
| /c                         | Create photo                |
| /a/:username               | Account page                |
| /a/:username/p             | Account photo feed          |
| /a/:username/p/:photo_id   | Photo page                  |
| /a/:username/e             | Account edit feed           |
| /a/:username/e/:edit_id    | Edit page                   |
+----------------------------+-----------------------------+
```

Templates are filled in using GraphQL to query for data.

There is API forwarding setup for these interfaces:

```
+-----------------------+-------------------+--------------+
| PUBLIC PATH           | FLASK PATH        | METHODS      |
+-----------------------+-------------------+--------------+
| /api/account          | /account          | PUT          |
| /api/photo            | /photo            | PUT          |
| /api/edit             | /edit             | PUT          |
| /api/reply            | /reply            | PUT          |
| /api/upvote           | /upvote           | PUT          |
| /api/preview          | /preview          | PUT          |
| /api/tag              | /tag              | PUT          |
| /api/editor           | /editor           | PUT          |
| /api/camera           | /camera           | PUT          |
| /api/lens             | /lens             | PUT          |
| /api/manufacturer     | /manufacturer     | PUT          |
| /api/account/:id      | /account/:id      | POST, DELETE |
| /api/photo/:id        | /photo/:id        | POST, DELETE |
| /api/edit/:id         | /edit/:id         | POST, DELETE |
| /api/reply/:id        | /reply/:id        | POST, DELETE |
| /api/upvote/:id       | /upvote/:id       | POST, DELETE |
| /api/preview/:id      | /preview/:id      | POST, DELETE |
| /api/tag/:id          | /tag/:id          | POST, DELETE |
| /api/editor/:id       | /editor/:id       | POST, DELETE |
| /api/camera/:id       | /camera/:id       | POST, DELETE |
| /api/lens/:id         | /lens/:id         | POST, DELETE |
| /api/manufacturer/:id | /manufacturer/:id | POST, DELETE |
|                     *  TO BE ADDED  *                    |
| /api/session          | /session          | POST         |
| /api/session          | /session          | DELETE       |
+-----------------------+-------------------+--------------+
```

### First time set up

System requirements:
    - Node >= 14
    - NPM >= 7

Install dependencies with NPM and you're good to go:

```bash
npm install
```

### Start the client

```bash
npm run dev
```

The website should become available at [http://localhost:3000](http://localhost:3000).
