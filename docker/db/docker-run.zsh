#!/bin/zsh

script_dir=$(dirname $0:A);
project_dir=$(dirname $(dirname $script_dir));

mkdir $project_dir/db

# Run mysql server at port 3306
docker run \
    -d \
    --name mysql \
    -e MYSQL_ROOT_PASSWORD=root \
    -v $project_dir/db:/var/lib/mysql \
    -p 3306:3306 \
    mysql
