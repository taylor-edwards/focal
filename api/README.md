# Focal

Focal is a place for photographers of all levels to learn and share editing techniques. Browse photos and download original files to submit your own edits, or share a photo to see how others would edit it!

Sharing raw images and sidecar files is an essential element of Focal. Working with original, uncompressed files gives people an opportunity to learn more about the cameras, lenses and editing software that enable digital photography.

## Codebase

The backend includes a PostgreSQL database and GraphQL interface assembled with SQLAlchemy, Graphene and Flask in between. The frontend is a web client written with the Next.js framework that uses server-side rendering (SSR) and the hydration model with React.

### First time set up

System requirements:
    - Python 3 with PIP and venv
    - PostgreSQL 14

Create a virtual environment and install dependencies:

```
python3 -m venv ./.venv
source ./.venv/bin/activate
pip3 install -r requirements.txt
```

Whenver you're done running Focal, remember to exit the virtual environment we activated with `source` in the above command:

```
# undo `source ./.venv/bin/activate`
deactivate
```

### Start the server

```
source ./.venv/bin/activate
python3 app.py
```

Now visit [localhost:5000/graphql](http://localhost:5000/graphql) to access the GraphiQL client. Press `Ctrl`+`c` to stop and enter `deactivate` to exit the virtual env.
