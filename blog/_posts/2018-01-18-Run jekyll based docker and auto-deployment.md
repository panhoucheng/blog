---
layout: post
title: 基于Docker搭建Jekyll并实现自动部署 
date: 2018-01-18 11:32:24.000000000 +09:00
tags: Plan
---
## 基于Docker搭建Jekyll并实现自动部署 

国内的服务器到期之后，博客就停了，最近打算重新启用起来，所以决定花了一天时间来重新搭建了一下。
先上地址:[https://xxblog.cn](https://xxblog.cn "XxBlog")

### 博客准备
博客是基于 [Jekyll](https://jekyllrb.com/ "Jekyll") 搭建的，然后主题使用了 @onevcat 大神修改的 [vno-jekyll](vno-jekyll "https://github.com/onevcat/vno-jekyll") ,一直很喜欢这种风格的博客，好了，开始正题。

### Docker

既然jekyll是一个独立的服务，那么选择基于docker来运行它是自然了的。
##### Dockerfile
<pre>
<code>
FROM ruby:latest
RUN gem install jekyll bundler
COPY blog /blog/
RUN cd blog \
         && bundler install
WORKDIR /blog
CMD bundle exec jekyll serve --host 0.0.0.0

</pre>
</code>
这里我遇到了一个大坑，最后一行启动jekyll的命令`bundle exec jekyll serve --host 0.0.0.0`，默认如果不加 `--host 0.0.0.0`,
程序只绑定了127.0.0.1端口，使用Docker -p 4000:4000无法成功映射，找了很久的原因才发现，docker映射端口之后，是使用了宿主机的IP地址去访问 container 中的服务的，所以自然是访问不了只绑定了127.0.0.1的端口咯，再贴上 docker-compos文件。
##### docker-compose.yml
<pre>
<code>
version: '3'
services:
  blog:
      build: .
      image: jekyll/blog:latest
      ports:
   		- "14000:4000"
      networks:
        - test-net
networks:
  test-net:
</pre>
</code>

然后每次我都只需要 pull 一下Git远端仓库的更新，然后重新 build 一下docker image 就可以了。

### 自动部署

本来到了这里博客就已经可以通过Docker来运行了，但是爱折腾的我怎么能就这样停止了呢？ 每次写完文章都要手动登录到服务器执行这么多行命令实在是太不方便了。我最想要的方式还是在本地写好了文章， push 到 Git 远程仓库，然后网站就自动更新。、
说干就干，首先把更新文章，构建镜像然后启动这些步骤都写到一个 shell 文件里面去。
##### build.sh
<pre>
<code>
#!/bin/bash
docker-compose down \
        && git pull origin master \
        && docker-compose build \
        && docker-compose up -d
</pre>
</code>

每次只需要执行以下./build.sh就可以实现自动更新，构建，重启了，但是这样还是需要手动登录到服务器执行命令，如果我们连这一步都想要省去 呢？ OK 配合 Git 的 Webhook就可以实现。
首先我们需要在服务器上面启动一个 http 服务，这么简单的一个需求，就用 python 来实现吧。

##### webhook.py

<pre>
<code>
#!/usr/bin/env python
# coding=utf-8
from wsgiref.simple_server import make_server
import subprocess


def application(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])
    subprocess.Popen('/mnt/blog/build.sh')
    print('update success.')
    return [b'success, web hook!']


httpd = make_server('127.0.0.1', 18000, application)
print('Serving HTTP on port 18000...')
httpd.serve_forever()
</pre>
</code>

然后再通过 ` nohub python webhook.py &` 后台运行这个 python 程序就可以了。最好再把这条命令设置成开机启动。

教程完成，就当给自己记录一下吧。