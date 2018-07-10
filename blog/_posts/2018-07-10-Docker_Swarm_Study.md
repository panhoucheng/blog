---
layout: post
title: Docker Swarm 配置
date: 2018-07-10 11:32:24.000000000 +09:00
tags: docker swarm
---
## Docker Swarm 配置

1. 初始化Docker swarm Master节点，可以得到集群的Token。
	```shell
	docker swarm init --advertise-addr 192.168.242.129
	```
	运行之后如果没有出错可以得到下面的结果：
	```shell
	Swarm initialized: current node (f8xch6u685str1fjv7zvu7lxz) is now a manager.
	To add a worker to this swarm, run the following command:
    docker swarm join --token SWMTKN-1-4b6uw7iy6vxwnmv3fohyld7wjwebltz5u38tbc6mf3edlenher-0plmowly3qupmwcr2e8x40exx 192.168.242.129:2377
	To add a manager to this swarm, run 'docker swarm join-token manager' and follow the instructions.
	```

	> 注意：如果忘了docker swarm join 命令中的token的话，可以使用命令`docker swarm join-token worke`来找到
	
2. 在worker节点上运行加入集群命令。	
```shell
docker swarm join --token SWMTKN-1-4b6uw7iy6vxwnmv3fohyld7wjwebltz5u38tbc6mf3edlenher-0plmowly3qupmwcr2e8x40exx 192.168.242.129:2377	
```

3. 在集群上多节点运行容器。
```shell
docker service create --replicas 2 -d -p 8080:80 --name mynginx registry.docker-cn.com/library/nginx
```
4. 等待若干分钟后（每一个node都需要pull image），可以通过使用下面两条命令查出运行状态。
```shell
docker service ls
docker service ps mynginx
```


----------

### docker swarm常用命令：
* 扩容Service中的任务。
```
docker service scale mynginx=3
```
slave节点加入集群
```
docker swarm join --token [token] [master的IP]:[master的端口]
```
slave节点主动离开集群
```
docker swarm leave
```
master上创建service举例
```
docker service create --replicas 2 -d -p 8080:80 --name 服务名 镜像名
```
master上查看service信息
```
docker service ls
docker service ps 你所创建的服务的ID
```
在master上删除service
```
docker service rm 服务名
```
在master上进行服务扩容
```
docker service rm 服务名
```