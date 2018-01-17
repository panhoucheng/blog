---
layout: post
title: Tomcat配置Https证书
date: 2016-03-08 15:32:24.000000000 +09:00
---
###Tomcat配置Https证书
最近做项目的时候时候用到了Paypal支付，目前Paypal推荐使用RESTapi来发起支付，支付之后Paypal服务器会异步回调发起方的服务器，需要在Paypal Developer里面的DASHBOARD中配置WEBHOOKS地址，也就是回调地址，蛋疼的地方来了，Paypal的回调接口地址必须使用Https开头，（国内的支付宝都可以使用http，真是蛋疼，或许这些地方就是Paypal在国内火不起来的一部分原因吧。）好了，废话不多说了，开始操作步骤：
####HTTPS证书

首先需要一张HTTPS证书，这个证书可以自己生成，也可以购买，当然自己生成的证书在浏览器中访问的时候浏览器会提示用户网站的证书不受信任，甚至部分浏览器不能访问。

那么就需要我们去购买一张证书了，当然目前有一些免费的https证书颁发机构，我就找了国内的沃通免费证书，生成很快，大搞10分钟就把证书申请下来了，设置密码，下载证书之后会有不同服务器端的证书，其他端请自行google如何绑定证书。

这里介绍Tomcat的，首先上传证书到服务器，存放在一个安全的路径下，然后进入Tomcat目录，进入conf目录，备份一下server.xml文件，然后编辑server.xml文件，找到下面的配置（默认被注释）。
<pre><code>
&lt;!--
    &lt;Connector port="8443" protocol="org.apache.coyote.http11.Http11NioProtocol"
               maxThreads="150" SSLEnabled="true" scheme="https" secure="true"
               clientAuth="false" sslProtocol="TLS" />
--></code>
</pre>
然后把注释符号删除，启用这段，修改port为https默认端口443，添加两个参数keystoreFile="证书文件位置",keystorePass="证书密码"。
<pre>
<code>
&lt;Connector port="443" protocol="org.apache.coyote.http11.Http11NioProtocol"
               maxThreads="150" SSLEnabled="true" scheme="https" secure="true"
               clientAuth="false" sslProtocol="TLS" keystoreFile="/home/*.jks" keystorePass="keyPassword"  /></code>
</pre>
到这部，如果配置正确，重启一下tomcat，应该就是可以通过
https://yourdomin.com
来访问了，当然这个时候是http和https都可以访问，如果需要将http请求自动跳转到https还需要对web.xml进行配置。
在tomcat\conf\web.xml中的</welcome-file-list>后面加上这样一段：
<pre>
<code>&lt;login-config>  
	    &lt;!-- Authorization setting for SSL -->  
	    &lt;auth-method>CLIENT-CERT</auth-method>  
	    &lt;realm-name>Client Cert Users-only Area&lt;/realm-name>  
	&lt;/login-config>  
	&lt;security-constraint>  
	    &lt;!-- Authorization setting for SSL -->  
	    &lt;web-resource-collection >  
	        &lt;web-resource-name >SSL&lt;/web-resource-name>  
	        &lt;url-pattern>/*&lt;/url-pattern>  
	    &lt;/web-resource-collection>  
	    &lt;user-data-constraint>  
	        &lt;transport-guarantee>CONFIDENTIAL&lt;/transport-guarantee>  
	    &lt;/user-data-constraint>  
	&lt;/security-constraint>  
</code></pre>
这样就大功搞成了，全站https。
教程就到这了，继续撸码。