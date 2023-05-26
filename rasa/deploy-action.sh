#!/bin/bash

today=` date "+%Y%m%d"`
abbrev=`git log|head -1|cut -b 8-14`
tag=$today-$abbrev
docker build -t registry-vpc.cn-beijing.aliyuncs.com/visva/bi_rasa_action:$tag -f Dockerfile-action .
if test `docker ps |grep bi_rasa_action|wc -l` == 1
 then
  echo 'container exists'
  docker rm -f bi_rasa_action
else
  echo 'container not  exists'
fi

if [ -n "$1" ] && [ "$1" = "push" ] ;then
  echo $1
  echo "registry-vpc.cn-beijing.aliyuncs.com/visva/bi_rasa_action:$tag to docker hub------"
  docker push registry-vpc.cn-beijing.aliyuncs.com/visva/bi_rasa_action:$tag
fi
