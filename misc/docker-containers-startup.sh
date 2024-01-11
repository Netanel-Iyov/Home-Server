#!/bin/bash

# start harbor compose
# cd /work/niyov/harbor/harbor-src && sudo docker-compose up -d
cd $1 && sudo docker-compose up -d

# start nginx
# sleep 10 && cd /work/niyov/repos/Home-Server/nginx && docker-compose restart
sleep 10 && cd $2 && docker-compose restart