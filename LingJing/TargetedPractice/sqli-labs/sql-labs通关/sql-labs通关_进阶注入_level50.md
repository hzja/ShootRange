## sqli-labs第五十关

五十关和四十六关一样，可以使用updatexml进行报错注入，不过这个里面还可以使用堆叠注入，因为使用了mysqli_multi_query函数，支持多条sql语句执行。也可以延时注入。可以借鉴三十八代码

![](./img/861f275ca1eed50e34dece79ef6af964.png)

