#!/bin/zsh
script_dir=$(dirname $0:A);
package_path=$(dirname $script_dir);

[ ! -d "$package_path/db" ] && mkdir $package_path/db

# Run mysql server at port 3306
docker run \
    -d \
    --name mysql \
    -e MYSQL_ROOT_PASSWORD=root \
    -v $package_path/db:/var/lib/mysql \
    -p 3306:3306 \
    mysql &&
    echo "mysql database container running on port 3306"