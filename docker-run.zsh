#!/bin/zsh

script_path=$0:A;
project_path=$(dirname $script_path);
project_name=$(basename $project_path);

IMAGE_ID=${1:-jupyter-ds}
CONTAINER_ID=$project_name

DOCKER_HOST_URL=127.0.0.1

echo "Running '$CONTAINER_ID' container in detached mode, using '$IMAGE_ID' image:"

# Create container
if docker run -d -v $project_path/:/opt/project -p 8888:8888 --name $CONTAINER_ID $IMAGE_ID; then \
    SERVER_URL='';

    while [[ $SERVER_URL == '' ]] do
        SERVER_URL=$(docker exec $CONTAINER_ID jupyter notebook list | tail -1 | \
            grep -Eo 'http.* ::' | sed "s/0.0.0.0/$DOCKER_HOST_URL/g" | sed 's/ :://g');
    done

    echo "\nJupyter notebook server is running at:\n$SERVER_URL.\n\n"\
         "To stop and remove the container type in:\n"\
         "    docker stop $CONTAINER_ID\n"\
         "    docker rm $CONTAINER_ID"  \

fi