script_path=$0:A;
docker_path=$(dirname $script_path);
project_path=$(dirname $docker_path);
notebooks_path="$project_path/notebooks";

DOCKER_HOST_URL=$(echo $DOCKER_HOST | grep -Eo '\d.*:' | sed 's/://g');

echo "Running 'miniconda_jupyter' container in detached mode:"

if docker run -d -v $notebooks_path:/notebooks -p 8888:8888 miniconda_jupyter; then \
    CONTAINER_ID=$(docker ps -l | tail -1 | grep -Eo '^\w+');
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

