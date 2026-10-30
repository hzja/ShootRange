# LOW等级靶场通关

## Vulnerability: Brute Force

首先进行代码审计：

~~~ php
<?php
/**
 * DVWA 登录模块（低安全级别）
 * 功能：通过 GET 接收用户名和密码，查询数据库验证登录。
 * 注意：此代码存在严重的 SQL 注入漏洞，仅用于教学靶场，不可用于生产环境。
 */

// 判断是否提交了登录请求（GET 参数 Login）
if( isset( $_GET[ 'Login' ] ) ) {
    // 获取用户名（未做任何过滤，直接用于 SQL 拼接）
    $user = $_GET[ 'username' ];

    // 获取密码
    $pass = $_GET[ 'password' ];
    // 对密码进行 MD5 哈希（不安全，生产环境应使用 password_hash）
    $pass = md5( $pass );

    // 直接拼接 SQL 查询语句，存在 SQL 注入漏洞
    $query  = "SELECT * FROM `users` WHERE user = '$user' AND password = '$pass';";

    // 执行查询；如果失败则输出数据库错误信息并终止脚本
    $result = mysqli_query($GLOBALS["___mysqli_ston"],  $query ) or die( '<pre>' . ((is_object($GLOBALS["___mysqli_ston"])) ? mysqli_error($GLOBALS["___mysqli_ston"]) : (($___mysqli_res = mysqli_connect_error()) ? $___mysqli_res : false)) . '</pre>' );

    // 如果查询成功，并且恰好返回一行记录，说明用户名和密码匹配
    if( $result && mysqli_num_rows( $result ) == 1 ) {
        // 获取该用户的信息（关联数组）
        $row    = mysqli_fetch_assoc( $result );
        // 取出头像字段
        $avatar = $row["avatar"];

        // 登录成功，输出欢迎信息和用户头像
        echo "<p>Welcome to the password protected area {$user}</p>";
        echo "<img src=\"{$avatar}\" />";
    }
    else {
        // 登录失败，输出通用错误提示
        echo "<pre><br />Username and/or password incorrect.</pre>";
    }

    // 关闭数据库连接
    ((is_null($___mysqli_res = mysqli_close($GLOBALS["___mysqli_ston"]))) ? false : $___mysqli_res);
}

?>
~~~



另外：

~~~ php
// 执行 SQL 查询：
//   - 第一个参数 $GLOBALS["___mysqli_ston"] 是全局的 mysqli 数据库连接对象（DVWA 兼容写法）
//   - 第二个参数 $query 是要执行的 SQL 语句
//   - 如果 mysqli_query 执行失败（返回 false），则通过 "or die(...)" 终止脚本并输出错误信息
$result = mysqli_query($GLOBALS["___mysqli_ston"],  $query ) or die(
    '<pre>' . 
    (
        // 判断全局连接变量是否是一个对象
        (is_object($GLOBALS["___mysqli_ston"]))
            // 如果是对象，说明连接已建立，使用 mysqli_error() 获取最近一次 MySQL 操作的错误信息
            ? mysqli_error($GLOBALS["___mysqli_ston"])
            // 如果不是对象，说明连接可能未建立，尝试用 mysqli_connect_error() 获取连接错误
            : (
                // 将 mysqli_connect_error() 的返回值赋给 $___mysqli_res
                ($___mysqli_res = mysqli_connect_error())
                    // 如果连接错误信息存在（非空），则输出该错误信息
                    ? $___mysqli_res
                    // 否则返回 false（最终拼接为空字符串）
                    : false
              )
    ) . 
    '</pre>'
    // 最终输出形如 <pre>错误信息</pre> 的内容，方便在网页上显示
);
~~~

~~~ php
// 关闭数据库连接：
//   - 调用 mysqli_close() 关闭全局 MySQLi 连接对象 $GLOBALS["___mysqli_ston"]
//   - 将关闭操作的返回值（成功为 true，失败为 false）赋给变量 $___mysqli_res
//   - 然后判断 $___mysqli_res 是否为 null：
//       - 如果为 null，则三元表达式返回 false
//       - 否则返回 $___mysqli_res（即 true 或 false）
//   - 整个表达式的结果并未被使用，这行代码的实际作用仅仅是执行 mysqli_close() 来关闭连接
//   - 这种写法通常是 MySQL 转 MySQLi 自动转换工具生成的兼容代码，可简化为：
//         mysqli_close($GLOBALS["___mysqli_ston"]);
((is_null($___mysqli_res = mysqli_close($GLOBALS["___mysqli_ston"]))) ? false : $___mysqli_res);
~~~



首先进入原始画面使用<code>BurpSuite</code>进行拦截

![BruteForce_01](.\img\Low_BruteForce_01.PNG)

右键点击<code>send to Intruder</code>准备开始暴力破解



进入<code>Intruder</code>界面，分析需要爆破的点只有一个就是<code>password</code>参数。因为之前已经确认有<code>admin</code>用户，所以可以只针对<code>password</code>参数进行爆破。

+ 选择<code>Sniper attack</code>
+ 在<code>password</code>参数处清空原先参数后右键点击<code>add payload position</code>添加<code>payload</code>点，如下图所示
+ 选中<code>payload</code>点，在右边的界面中点击<code>Load</code>加载爆破字典
+ 点击<code>Start attack</code>开始爆破攻击

![BruteForce_02](.\img\Low_BruteForce_02.PNG)



攻击结束后，查看返回字节长度<code>Length</code>那一栏，与其他项不同的那个就是爆破命中了

![BruteForce_03](.\img\Low_BruteForce_03.PNG)

由此可知，对应的<code>payload</code>是<code>password</code>



所以使用<code>admin/password</code>即可成功登录

![BruteForce_04](.\img\Low_BruteForce_04.PNG)



## Vulnerability: Command Injection

~~~ php
<?php
/**
 * DVWA 命令注入模块（低安全级别）
 * 功能：接收用户输入的 IP 地址，执行 ping 命令并返回结果。
 * 注意：此代码存在严重的命令注入漏洞，仅用于教学靶场，不可用于生产环境。
 */

// 判断是否提交了表单（POST 参数 Submit）
if( isset( $_POST[ 'Submit' ]  ) ) {
    // 获取用户输入的 IP 地址
    // 使用 $_REQUEST 可以接收 GET 或 POST 参数，未做任何过滤
    $target = $_REQUEST[ 'ip' ];

    // 判断当前操作系统类型，以决定使用哪种 ping 命令格式
    // php_uname('s') 返回操作系统名称，stristr 不区分大小写查找 'Windows NT'
    if( stristr( php_uname( 's' ), 'Windows NT' ) ) {
        // Windows 系统：执行 ping 命令
        // 直接将用户输入拼接到命令中，没有进行任何转义或过滤
        // 攻击者可以通过 ;、&&、| 等符号注入任意系统命令
        $cmd = shell_exec( 'ping  ' . $target );
    }
    else {
        // *nix 系统（Linux、Unix 等）：执行 ping 命令，-c 4 表示发送 4 个包
        // 同样直接拼接用户输入，存在命令注入漏洞
        $cmd = shell_exec( 'ping  -c 4 ' . $target );
    }

    // 将命令执行结果输出到页面，包裹在 <pre> 标签中
    echo "<pre>{$cmd}</pre>";
}

?>
~~~

进行代码审计，可知输入的<code>IP</code>地址可直接拼接到命令中执行



输入的<CODE>ip</CODE>即是<code>payload</code>为<code>127.0.0.1 && whoami</code>，命令成功执行

![](.\img\Low_CommandInjection_01.PNG)



## Vulnerability: Cross Site Request Forgery (CSRF)

+ 先输入不同代码，查看有何不一样的地方

![Low_CSRF_01](.\img\Low_CSRF_01.PNG)

对应的链接为<code>http://192.168.242.53/vulnerabilities/csrf/?password_new=123&password_conf=456&Change=Change#</code>



+ 修改链接为<code>http://192.168.242.53/vulnerabilities/csrf/?password_new=123&password_conf=123&Change=Change#</code>，重新在新界面打开该链接，发现密码已经被修改成功

![Low_CSRF_02](.\img\Low_CSRF_02.PNG)