#!/bin/zsh
script_dir=$(dirname $0:A);
package_path=$(dirname $script_dir);
project_path=$(dirname $(dirname $package_path));

[ ! -d "$project_path/db" ] && mkdir $project_path/db

# Run mysql server at port 3306
docker run \
    -d \
    --name mysql \
    -e MYSQL_ROOT_PASSWORD=root \
    -v $project_dir/db:/var/lib/mysql \
    -p 3306:3306 \
    mysql
