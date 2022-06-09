# Simple API example with Postgres + Redis

## What?

This is an example code to self-host an API with a local Postgres and redis installation, the project contains:

- Example Python FastAPI code

- Nginx rev-proxy to load balance between two servers

- Dockerfile to package and deploy the Python API

- Redis

- PostgresSQL DB

- Docker Compose file for local development.

## How?

To bring the stack up:

```
docker-compose build && docker-compose up
```

To bring the stack down:
```
docker-compose down
```

The compose file will create a docker volume to ensure that the DB is persisted across deployments, to wipe the db perform run: `docker volume rm $VOLUME_NAME`

### Scaling the stack

In order to scale the stack there are two main things to do BEFORE:

1. In the Nginx proxy config, `nginx.conf`, add another entry for another server:

```
upstream loadbalancer {
    # Using Round Robin as load balancing method
    server 172.17.0.1:5001;
    server 172.17.0.1:5002;
    server 172.17.0.1:$PORTNUMBER;
}
```

2. Add another container definition in the `docker-compose.yaml` file:

```
    fastapi$NUMBER:
        build: app/.
        container_name: fastapi$NUMBER
        command: uvicorn app.main:app --host 0.0.0.0 --port $PORTNUMBER
        volumes:
            - ./app:/usr/src/app/
        ports:
            - "$PORTNUMBER:$PORTNUMBER"
        depends_on:
            - redis
            - postgres
        environment:
          - REDIS_HOST=host.docker.internal
          - REDIS_PORT=6379
```

Once the two steps described above are done, bring down the stack `docker-compose down` and bring it up again `docker-compose build && docker-compose up`