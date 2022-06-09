# Simple API example with Postgres + Redis

## What?

This is an example code to self-host an API with a local Postgres and redis installation, the project contains:

- Example Python FastAPI code

- Dockerfile to package and deploy the Python API

- Docker compose file controlling all the stack

## How?

To bring the stack up:

```
docker-compose up -d
```

To bring the stack down:
```
docker-compose down
```

The compose file will create a docker volume to ensure that the DB is persisted across deployments, to wipe the db perform run: `docker volume rm $VOLUME_NAME`