#!/bin/bash

today=` date "+%Y%m%d"`
abbrev=`git log|head -1|cut -b 8-14`
tag=$today-$abbrev
docker build -t registry-vpc.cn-beijing.aliyuncs.com/visva/bi_qa:$tag .
if test `docker ps |grep bi_qa|wc -l` == 1
 then
  echo 'container exists'
  docker rm -f bi_qa
else
  echo 'container not  exists'
fi

if [ -n "$2" ] && [ "$2" = "push" ] ;then
  echo $2
  echo "registry-vpc.cn-beijing.aliyuncs.com/visva/bi_qa:$tag to docker hub------"
  docker push registry-vpc.cn-beijing.aliyuncs.com/visva/bi_qa:$tag
fi
