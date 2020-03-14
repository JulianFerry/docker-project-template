#!/bin/zsh

script_dir=$(dirname $0:A);
project_path=$(dirname $(dirname $script_dir));
project_name=$(basename $project_path);

export DOCKER_BUILDKIT=1

# Stop and remove project container if it exists. Remove image if it exists
docker ps | grep -q $project_name       && docker stop $project_name;
docker ps -a | grep -q $project_name    && docker rm $project_name;
docker image ls | grep -q $project_name && docker rmi -f $project_name;

# Build project image and run new container
docker build -t $project_name -f $script_dir/Dockerfile $project_path
if docker run -d --name $project_name -p 8080:8080 $project_name; then
    echo "Container '$project_name' up and running at port 8080!"
fi
