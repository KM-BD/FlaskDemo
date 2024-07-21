#!/usr/bin/env sh

set -x
# Remove existing container if it exists
docker rm -f my-apache-php-app || true
docker run -d -p 80:80 --name my-apache-php-app -v /mnt/c/Mods/Y2T3/SSD/Own Github/FlaskDemo/src:/var/www/html php:7.2-apache
sleep 1
set +x

echo 'Now...'
echo 'Visit http://localhost to see your PHP application in action.'