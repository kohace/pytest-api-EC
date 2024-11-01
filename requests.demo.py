import requests
from requests import utils

url = 'http://127.0.0.1:8787//dar/user/login'

header = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}

data = {
    "user_name": "test01",
    "passwd": "admin123",
}

#根据代码内容编写
res = requests.post(url, data=data)

print(res.text)
print(res.json())

session = requests.session()
res_3 = session.request("post", url, data,header)


utils.dict_from_cookiejar()