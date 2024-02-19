import requests
url = "http://192.168.31.126:8080/upload-labs/upload/EighteenSecondMethod.php"
while True:
    response = requests.get(url)
    if response.status_code == 200:
        print("ok")
        break