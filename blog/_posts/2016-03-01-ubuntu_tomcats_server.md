---
layout: post
title: Ubuntu配置多个Tomcat服务器
date: 2016-03-01 15:32:24.00 +09:00
---

###Ubuntu配置多个Tomcat服务器
最近参加了一个比赛项目，做服务端，打算把服务暂时部署在自己的服务器上面提供给安卓端的同学测试使用，我的服务端是Ubuntu+Nginx+Tomcat的，然后为了不影响服务器上面以前的其他项目，所以复制了一个Tomcat，下面就用Tomcat7070来描述这个新的Tomcat吧，然后简单的修改了一下：
	
	/Tomcat_Home/conf/server.xml

这个文件，然后启动了之后一直无法访问，后台测试了好久，把之前的Tomcat8080停了之后再启动新的Tomcat7070惊奇的发现启动的居然还是之前的Tomcat8080，所以便上网查了一下，发现原来Tomcat在启动的时候回自动向

	/etc/profile
文件中写入了一个

	export TOMCAT_HOME=/home/ubuntu/java/tomcat
	
###解决方案
经过一番百度，找到了解决方案

* 首先：修改profile文件，然后保存退出
	<pre>
export JAVA_HOME=/usr/lib/jvm
export CALSSPATH=$JAVA_HOME/lib/*.*
export PATH=$PATH:$JAVA_HOME/bin
\#tomcat
  CATALINA_HOME=/home/ubuntu/java/tomcat
CATALINA_BASE=/home/ubuntu/java/tomcat
export CATALINA_BASE CATALINA_HOME
\#tomcat2_7070
  CATALINA_2_HOME=/home/ubuntu/java/tomcat-qingning-7070
CATALINA_2_BASE=/home/ubuntu/java/tomcat-qingning-7070
export CATALINA_2_BASE CATALINA_2_HOME

  export TOMCAT_HOME=/home/ubuntu/java/tomcat

  export TOMCAT_2_HOME=/home/ubuntu/java/tomcat-qingning-7070
</pre>

* 修改第二个Tomcat，也就是Tomcat7070中的Server.xml的shutdown端口和connector端口：

	<pre>/tomcat_home/conf/server.xml</pre>

		<Server port="8006" shutdown="SHUTDOWN">
		<Connector port="7070" protocol="HTTP/1.1"
               connectionTimeout="20000"
               redirectPort="8443" />
* 修改Tomcat2也就是Tomcat7070的启动关闭配置,路径为：
	<pre>/tomcat_home/bin/startup.sh
/tomcat_home/bin/shutdown.sh</pre>

	修改方法为分别在两个配置文件中加入下面两行代码：
	
	<pre>export CATALINA_HOME=$CATALINA_2_HOME
export CATALINA_BASE=$CATALINA_2_BASE</pre>

###然后就搞定了！，访问localhost:7070看看效果吧!		

