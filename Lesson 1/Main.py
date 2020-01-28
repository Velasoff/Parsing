# from pprint import pprint
import requests
import json
import os.path
user = 'Velasoff'
main_link = 'https://api.github.com/users/' + user + '/repos'
auth_link = 'https://api.github.com/user'
# header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}

if os.path.exists("C:/path/kw.DAT"):
    with open("C:/path/kw.DAT", "r") as f:
        key = f.read()
    response_login = requests.get(auth_link, auth=(user, key))
    data = json.loads(response_login.text)
    with open("request_auth.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)
else:
    key = ''

response = requests.get(main_link)
if response.ok:
    data = json.loads(response.text)
    # pprint(data)
    # for i in data:
    #     pprint(i)
    with open("request.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)
    print(f"У пользователя {user} на Github количество репозиториев равно {len(data)}, названиями:", end='\n\t')
    for i in data:
        print(i["name"], end='\n\t')