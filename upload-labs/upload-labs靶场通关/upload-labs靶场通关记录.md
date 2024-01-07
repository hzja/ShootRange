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

