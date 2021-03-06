---
layout: post
title: 如何获取真实的客户端IP(防止客户端伪造)
date: 2019-09-26 16:32:24.000000000 +08:00
---

# 利用X-Forwarded-For伪造客户端IP漏洞成因及防范

## 问题背景
在Web应用开发中，经常会需要获取客户端IP地址。一个典型的例子就是投票系统，为了防止刷票，需要限制每个IP地址只能投票一次。

## 如何获取客户端IP
在Java中，获取客户端IP最直接的方式就是使用 `request.getRemoteAddr()` ，这种方式能获取到连接服务器的客户端IP，在中间没有代理的情况下，的确是最简单有效的方式。但是目前互联网 Web 应用很少会将应用服务器直接对外提供服务，一般都会有一层Nginx做反向代理和负载均衡，有的甚至可能有多层代理。在有反向代理的情况下，直接使用`request.getRemoteAddr()`获取到的IP地址是Nginx所在服务器的IP地址，而不是客户端的IP。

HTTP协议是基于TCP协议的，由于`request.getRemoteAddr()`获取到的是TCP层直接连接的客户端的IP，对于Web应用服务器来说直接连接它的客户端实际上是Nginx，也就是TCP层是拿不到真实客户端的IP。
为了解决上面的问题，很多HTTP代理会在HTTP协议头中添加X-Forwarded-For头，用来追踪请求的来源。`X-Forwarded-For`的格式如下：
```
X-Forwarded-For: client1, proxy1, proxy2
```

`X-Forwarded-For`包含多个IP地址，每个值通过逗号+空格分开，最左边（client1）是最原始客户端的IP地址，中间如果有多层代理，每一层代理会将连接它的客户端IP追加在X-Forwarded-For右边。

下面就是一种常用的获取客户端真实IP的方法，首先从HTTP头中获取X-Forwarded-For，如果X-Forwarded-For头存在就按逗号分隔取最左边第一个IP地址，不存在直接通过`request.getRemoteAddr()`获取IP地址：
```
public String getClientIp(HttpServletRequest request) { 
    String xff = request.getHeader("X-Forwarded-For"); 
    if (xff == null) { 
        return request.getRemoteAddr();    
    } else { 
        return xff.contains(",") ? xff.split(",")[0] : xff;    
    }
}
```
另外，要让Nginx支持`X-Forwarded-For`头，需要配置：
```
proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
```
`$proxy_add_x_forwarded_for`会将和Nginx直接连接的客户端IP追加在请求原有X-Forwarded-For值的右边。
## 伪造X-Forwarded-For

一般的客户端（例如浏览器）发送HTTP请求是没有`X-Forwarded-For`头的，当请求到达第一个代理服务器时，代理服务器会加上`X-Forwarded-For`请求头，并将值设为客户端的IP地址（也就是最左边第一个值），后面如果还有多个代理，会依次将IP追加到`X-Forwarded-For`头最右边，最终请求到达Web应用服务器，应用通过获取X-Forwarded-For头取左边第一个IP即为客户端真实IP。

但是如果客户端在发起请求时，请求头上带上一个伪造的`X-Forwarded-For`，由于后续每层代理只会追加而不会覆盖，那么最终到达应用服务器时，获取的左边第一个IP地址将会是客户端伪造的IP。也就是上面的Java代码中`getClientIp()`方法获取的IP地址很有可能是伪造的IP地址，如果一个投票系统用这种方式做的IP限制，那么很容易会被刷票。
伪造`X-Forwarded-For`头的方法很简单，例如Postman就可以轻松做到：
![116a2a08b9abce4602a2c7ec61c3c74e.jpeg](https://image-file-1253433880.cos.ap-chengdu.myqcloud.com/blog/get_ip_by_java.jpg)

当然你也可以写一段刷票程序或者脚本，每次请求时添加`X-Forwarded-For`头并随机生成一个IP来实现刷票的目的。

## 如何防范

在直接对外的Nginx反向代理服务器上配置：
```
proxy_set_header X-Forwarded-For $remote_addr;
```
如果有多层Nginx代理，内层的Nginx配置：
```
proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
```
在最外层Nginx（即直接对外提供服务的Nginx）使用`$remote_addr`代替上面的`$proxy_add_x_forwarded_for`，可以防止伪造X-Forwarded-For。`$proxy_add_x_forwarded_for`会在原有`X-Forwarded-For`上追加IP，这就相当于给了伪造X-Forwarded-For的机会。而$remote_addr是获取的是直接TCP连接的客户端IP，这个是无法伪造的，即使客户端伪造也会被覆盖掉，而不是追加。

需要注意的是，如果有多层代理，只在直接对外访问的Nginx上配置`X-Forwarded-For`为`$remote_addr`，内层的Nginx还是要配置为`$proxy_add_x_forwarded_for`，不然内层的Nginx又会覆盖掉客户端的真实IP。

完成以上配置后，业务代码中再通过上面的`getClientIp()`方法，获取`X-Forwarded-For`最左边的IP地址即为真实的客户端地址，且客户端也无法伪造。