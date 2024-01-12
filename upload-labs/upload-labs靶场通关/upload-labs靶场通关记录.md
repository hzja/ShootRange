# upload-labs靶场通关



+ 源码位置：https://github.com/c0ny1/upload-labs

+ 参考通关秘籍：[Upload-labs靶场通关攻略(全网最全最完整)](https://blog.csdn.net/weixin_47598409/article/details/115050869)或者[Upload-labs靶场通关笔记(含代码审计)](https://blog.csdn.net/weixin_54894046/article/details/127239720?ops_request_misc=%7B%22request%5Fid%22%3A%22170438292316800215095603%22%2C%22scm%22%3A%2220140713.130102334..%22%7D&request_id=170438292316800215095603&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~top_positive~default-3-127239720-null-null.142^v99^control&utm_term=upload-labs通关&spm=1018.2226.3001.4187)
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
