# Docker Events PushBullet
Receive PushBullet notifications when on docker container events

## How it works
This image connects to the host machine socket, through a volume mapping, and listen [Docker Events API](https://docs.docker.com/engine/reference/api/docker_remote_api_v1.24/#/monitor-dockers-events).

When specified events are triggered it sends the affected containers' information to PushBullet.  

If no events are specified in the enironment variables, these are the default ones: "create","update","destroy","die","kill","pause","unpause","start","stop"

## Build
You must [create a release tag](https://git-scm.com/book/en/v2/Git-Basics-Tagging) in order to build and publish this image.
```shell
./build-all.sh
```

## Run
First get a PushBullet [Access Token](https://www.pushbullet.com/#settings)

### Run (default events)
```shell
docker run \
    -d --restart=always \
    -v /var/run/docker.sock:/var/run/docker.sock \
    -e PB_API_KEY="INSERT-KEY-HERE" \
    jmc265/docker-events-pushbullet:latest
```

### Run (custom events)
```shell
docker run \
    -d --restart=always \
    -v /var/run/docker.sock:/var/run/docker.sock \
    -e PB_API_KEY="INSERT-KEY-HERE" \
    -e EVENTS="die,destroy,kill"
    jmc265/docker-events-pushbullet:latest
```

## License
Apache License Version 2.0
