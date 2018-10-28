xhost +local:docker
docker run -it --rm \
    --user $(id -u):$(id -g) \
    --net=host -e DISPLAY \
    --volume $PWD/stylus-tracking:/stylus-tracking \
    jjanzic/docker-python3-opencv:contrib \
    python3 stylus-tracking
    # /bin/bash
