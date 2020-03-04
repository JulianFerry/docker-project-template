script_path=$0:A;
docker_path=$(dirname $script_path);
project_path=$(dirname $docker_path);
project_name=$(basename $project_path);

IMAGE_ID=${1:-miniconda_jupyter}
CONTAINER_ID=${1:-$project_name-v0}

DOCKER_HOST_URL=$(echo $DOCKER_HOST | grep -Eo '\d.*:' | sed 's/://g');

echo "Running '$CONTAINER_ID' container in detached mode, using '$IMAGE_ID' image:"

# Create 'dockerhost' network if it doesn't exist
docker network inspect dockerhost_net  >/dev/null 2>&1 || docker network create dockerhost_net

# Create container
if docker run -d -v $project_path:/project -p 8888:8888 --name $CONTAINER_ID --net=dockerhost_net $IMAGE_ID; then \
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

