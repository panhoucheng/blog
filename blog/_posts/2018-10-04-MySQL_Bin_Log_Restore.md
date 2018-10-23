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
docker service scale 服务名 = count
```
查看所有节点信息
```
docker node ls
```

##常用命令
* docker-machine 常用命令

|命令|说明|
|----|---|
|docker-machine create|	创建一个 Docker 主机（常用-d virtualbox）
|docker-machine ls|	查看所有的 Docker 主机
|docker-machine ssh	SSH| 到主机上执行命令
|docker-machine env|	显示连接到某个主机需要的环境变量
|docker-machine inspect|	输出主机更多信息
|docker-machine kill|	停止某个主机
|docker-machine restart|	重启某台主机
|docker-machine rm|	删除某台主机
|docker-machine scp|	在主机之间复制文件
|docker-machine start|	启动一个主机
|docker-machine status|	查看主机状态
|docker-machine stop|	停止一个主机

* docker swarm 常用命令

|命令|说明|
|----|---|
|docker swarm init	|初始化集群
|docker swarm join-token worker|查看工作节点的 token
|docker swarm join-token manager	|查看管理节点的 token
|docker swarm join	|加入集群中

* docker node 常用命令

|命令|说明|
|----|---|
|docker node ls|	查看所有集群节点
|docker node rm|	删除某个节点（-f强制删除）
|docker node inspect|	查看节点详情
|docker node demote|	节点降级，由管理节点降级为工作节点
|docker node promote|	节点升级，由工作节点升级为管理节点
|docker node update|	更新节点
|docker node ps|	查看节点中的 Task 任务

* docker service 常用命令

|命令|说明|
|----|---|
|docker service create|	部署服务
|docker service inspect|	查看服务详情
|docker service logs|	产看某个服务日志
|docker service ls|	查看所有服务详情
|docker service rm|	删除某个服务（-f强制删除）
|docker service scale name = count |	设置某个服务个数
|docker service update|	更新某个服务

* docker stack 常用命令

|命令|说明|
|----|---|
|docker stack deploy|	部署新的堆栈或更新现有堆栈
|docker stack ls|	列出现有堆栈
|docker stack ps|	列出堆栈中的任务
|docker stack rm|	删除堆栈
|docker stack services|	列出堆栈中的服务
|docker stack down|	移除某个堆栈（不会删除数据）

参考资料：
> [Docker官方指南 ](https://docs.docker.com/get-started "Docker Get Started")

> [Docker 三剑客之 Docker Swarm](https://www.cnblogs.com/xishuai/p/docker-swarm.html "Docker 三剑客之 Docker Swarm")