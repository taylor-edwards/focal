![Focal](web/public/focal-pics.png?raw=true "Focal")

Focal is a place for photographers of all levels to learn and share digital photo editing workflows. Browse photos and use their raw files to share your editing process, or upload a photo of your own to see how other people would edit it. Learn how to use a variety of photo editing software, from technique to fine art.

Sharing raw images and sidecar files is an essential element of Focal. Working with original, uncompressed files gives people an opportunity to learn more about the cameras, lenses and editing software that enable modern digital photography. Learn more about the editing software you use and find out what can be done with other editors on Focal.

## Codebase

The `/api` directory contains a Flask app which handles connections to the database and hosts a GraphQL endpoint using SQLAlchemy and Graphene. The `/web` directory contains a Next.JS app that runs the website. These are both built as Docker images and ran with docker-compose alongside a PostgreSQL database and NGINX.

## First time set up

To run Focal on your machine, you'll need a few things installed first:

* Python 3
* Node 12+
* Docker

1. Create a virtualenv and install Python dependencies with pip:
```sh
cd ./api
python3 -m venv ./.venv
source ./.venv/bin/activate
pip3 install -r requirements.txt
deactivate
```

2. Install Node dependencies and run an initial build to create directories:
```sh
cd ./web
npm install
npm run build
```

3. Create a file named `.env` and make sure these variables are defined in it (the production file can be found 1Password):
```sh
# /.env
POSTGRES_DB=my_db
POSTGRES_USER=my_user
POSTGRES_PASSWORD=my_password

# You only need these in production:
# SENDGRID_API_KEY=
# SIGN_IN_SENDGRID_TEMPLATE_ID=
# DELETE_ACCOUNT_SENDGRID_TEMPLATE_ID=
```

4. Enable BuildKit by setting these environment variables (only required for building the production web image):
```sh
export DOCKER_BUILDKIT=1
export COMPOSE_DOCKER_CLI_BUILD=1
```

5. Append these lines to your hosts file or create DNS records locally for them:
```sh
# /etc/hosts
127.0.0.1    local.pics
127.0.0.1    api.local.pics
127.0.0.1    cdn.local.pics
```

Now that you're set up, continue on below to start running a local instance.

## Running a local instance

Build and start all services for local development:
```sh
docker-compose -f docker-compose.yml -f dev.docker-compose.yml up
```

Access the web app at [local.pics:8080](http://local.pics:8080) and explore the data set at [local.pics:8080/graphql](http://local.pics:8080/api/graphql). You can make modifications to the API server and web app in the /api and /web directories respectively.

Restart a container without stopping the whole cluster:
```sh
docker restart focal_api_1
```

Reload NGINX configuration (while running):
```sh
docker exec -it focal_proxy_1 sh -c "/etc/init.d/nginx reload"
```

Start an interactive session within the database container:
```sh
docker exec -it focal_db_1 psql focal -U focal_api
```

## Production builds and deployment

1. Use Docker Compose to create and test production images:
```sh
docker-compose up --build
# should generate images named focal_api and focal_web
```

2. Tag and push verified images to the private Docker Registry (must be on VPN to resolve domain name):
```sh
docker tag focal_api docker.focal.pics/focal_api
docker push docker.focal.pics/focal_api
```

3. Restart affected containers:
```sh
DOCKER_HOST="ssh://docker@docker.focal.pics" docker-compose pull && docker-compose up --detach
```

## Managing dependencies

Dependencies are locally managed in development by directly running `pip` and `npm` commands. You do not have to stop or restart the app while in development mode when changing dependencies. In production, dependent modules are baked into images to ensure reproducibility.

### For Python - Flask API server

To import a new dependency in the Flask app, use `pip` from the API directory (substituting `flask` for your dependency):
```sh
cd ./api
source ./.venv/bin/activate
pip3 install flask
pip3 freeze > requirements.txt
deactivate
```

Make sure to commit the changes this made to the `requirements.txt` file.

If there is a new dependency added by someone else (or `requirements.txt` changed), you should run install again:
```sh
cd ./api
source ./.venv/bin/activate
pip3 install -r requirements.txt
deactivate
```

### For Node - Next app server

To import a new dependency in the Next app, use `npm` from the web directory (substituting `next` for your dependency):
```sh
cd ./web
npm install -D next
```

Make sure to commit the changes this made to the `package.json` and `package-lock.json` files.

If there is a new dependency added by someone else (or `package-lock.json` changed), you should run install again:
```sh
cd ./web
npm install
```
