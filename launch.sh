xhost +local:docker
docker run -it --rm \
    --user $(id -u):$(id -g) \
    --net=host -e DISPLAY \
    --volume $PWD/stylus_tracking:/myapp/stylus_tracking \
    -e PYTHONPATH=/myapp \
    jjanzic/docker-python3-opencv:contrib \
    python3 /myapp/stylus_tracking
    # /bin/bash
