xhost +local:docker
docker run -it --rm \
    --privileged \
    --user $(id -u):$(id -g) \
    --net=host -e DISPLAY \
    --device /dev/video0 \
    --volume $PWD/stylus_tracking:/myapp/stylus_tracking \
    -e PYTHONPATH=/myapp \
    lpasselin/stylus-tracking \
    python3 /myapp/stylus_tracking
    # /bin/bash
