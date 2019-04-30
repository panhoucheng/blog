---
layout: post
title: Java日志框架
date: 2019-04-30 16:32:24.000000000 +09:00
tags: Java Log Frameworks Log4j Log4j2 Logback
---
# Java日志框架

Java 的日志框架多如牛毛，常见的有Apache Log4J, Apache Log4J2，Logback，我们如果选择一个高性能，易使用，对代码侵入性低的日志框架呢？
首先说到日志框架，不得不提SLF4J, SLF4J提供了一个标准化的抽象API，大多数框架都遵守这种规范来实现API。这使您能够在不更改代码的情况下更改日志框架。我们只需要将依赖关系更改为实现SLF4J接口的不同框架。

* * *

### Apache Log4j

Apache Log4j是一个非常古老的日志框架，但也是几年来最流行的一个。它引入了一些基本概念，如分层日志级别和日志记录器，这些概念仍然在现代日志框架中使用。
开发团队在2015年宣布了Log4j的生命终结。虽然很多遗留项目仍然使用它，但是如果您开始一个新项目，您应该选择本文中讨论的其他框架。
#### How To Use?
如果您想在应用程序中使用Log4j，您可以在下面的代码片段中看到所需的Maven依赖关系。

```xml
<dependency> 
    <groupId>log4j</groupId> 
    <artifactId>log4j</artifactId> 
    <version>1.2.17</version> 
</dependency>
```
Log4j本身不支持SLF4J。您还需要添加以下依赖项，以便能够通过标准化接口使用Log4j。

```xml
<dependency> 
    <groupId>org.slf4j</groupId> 
    <artifactId>slf4j-log4j12</artifactId> 
    <scope>test</scope> 
</dependency>
```
* * *

### Logback

Logback是由实现Log4j的同一开发人员编写的，目标是成为它的继任者。它遵循与Log4j相同的概念，但是被重写以提高性能、本地支持SLF4J，并实现其他一些改进，如高级过滤选项和日志配置的自动重装

该框架由三部分组成:

* logback-core
* logback-classic
* logback-access

Logback-core 提供了日志框架的核心功能。Logback-classic为核心功能增加了更多功能，例如对SLF4J的本地支持。logback-access将它与servlet容器集成在一起，这样您就可以使用它来编写HTTP访问日志。

#### How To Use?

您只需要定义对 logback-classic 的依赖关系。它包括了对 logback-core 和 SLF4J API的依赖。

```xml
<dependency> 
    <groupId>ch.qos.logback</groupId> 
    <artifactId>logback-classic</artifactId> 
    <version>1.2.3</version> 
</dependency>
```

默认情况下Logback不需要任何配置，它将所有调试级别或更高级别的日志消息写入标准输出。您可以使用 XML 或 Groovy 格式的自定义配置文件来更改它。

Logback使用与Log4j相同的概念。因此，即使使用不同的文件格式，它们的配置也非常相似。

```xml
<configuration> 
    <appender name="FILE" class="ch.qos.logback.core.FileAppender"> 
        <file>app.log</file> 
        <encoder> 
            <pattern>%d{HH:mm:ss,SSS} %-5p [%c] - %m%n</pattern> 
        </encoder> 
    </appender> 
    <logger name="org.hibernate.SQL" level="DEBUG" /> 
    <logger name="org.hibernate.type.descriptor.sql" level="TRACE" /> 
    <root level="info"> 
        <appender-ref ref="FILE" /> 
    </root> 
</configuration>
```
在添加了所需的依赖项并配置了Logback之后，可以使用它通过SLF4J API编写日志消息。因此，如果想从Logback提供的改进中获益，不需要更改任何代码就可以用Logback替换Log4j。

* * *
### Apache Log4j2

Apache Log4j2是这三个框架中最年轻的一个，它的目标是通过在Log4j上提供自己的改进来改进这两个框架，包括Logback中包含的一些改进，并避免Log4j和Logback的问题。

因此，与Logback一样，Log4j2提供了对SLF4J的支持，自动重新加载日志配置，并支持高级筛选选项。除了这些特性之外，它还允许基于lambda表达式对日志语句进行延迟计算，为低延迟系统提供异步日志记录器，并提供无垃圾模式，以避免垃圾收集器操作造成的任何延迟。

所有这些特性使Log4j2成为这三个日志框架中最先进和最快的。
#### How To Use?

Log4j2 将其API和实现分别打包。您可以使用log4j-api实现和构建应用程序，在运行时需要额外提供log4j-core，如果希望使用 SLF4J API，还需要依赖 log4j-slf4j-impl，它是两个框架之间的桥梁。

```xml
<dependency> 
    <groupId>org.apache.logging.log4j</groupId> 
    <artifactId>log4j-api</artifactId> 
    <version>2.11.1</version> 
</dependency> 
<dependency> 
    <groupId>org.apache.logging.log4j</groupId> 
    <artifactId>log4j-core</artifactId> 
    <version>2.11.1</version> 
    </dependency> 
<dependency> 
    <groupId>org.apache.logging.log4j</groupId> 
    <artifactId>log4j-slf4j-impl</artifactId> 
    <version>2.11.1</version> 
</dependency>
```
Log4j2的配置遵循与前面两个日志框架相同的原则，因此看起来非常相似。
```xml
<Configuration status="info"> 
    <Appenders> 
        <File name="FILE" fileName="app.log"> 
            <PatternLayout pattern="%d{HH:mm:ss.SSS} [%t] %-5level %logger{36} - %msg%n"/> 
        </File> 
    </Appenders> 
    <Loggers> 
        <Logger name="org.hibernate.SQL" level="DEBUG"> 
            <AppenderRef ref="FILE"/> 
        </Logger> 
        <Logger name="org.hibernate.type.descriptor.sql" level="TRACE"> 
            <AppenderRef ref="FILE"/> 
        </Logger> 
        <Root level="info"> 
            <AppenderRef ref="FILE"/> 
        </Root> 
    </Loggers> 
</Configuration>
```
* * *

### 结论

Log4j、Logback和Log4j2都是广泛使用的很好的日志记录框架。那么应该使用哪一个呢?

我推荐使用Log4j2，因为它是三种框架中速度最快、最先进的。但是如果性能不是您的最高优先级，那么Logback仍然是一个不错的选择。

