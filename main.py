#курсовая работа
#from tqdm import tqdm
#from tqdm import tqdm
#from time import sleep
import json
import datetime
import time
import urllib
import requests
from pprint import pprint

class YaUploader:
    def __init__(self, token: str):
        self.token = token

    def upload(self, file_path: str):
        """Метод загружает файлы по списку file_list на яндекс диск"""


        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)
        }
        files_url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        params = {'path': "Импорт_из_VK/"+file_path, 'overwrite': 'true'}
        response = requests.get(files_url, headers=headers, params=params)
        data = response.json()
        href = data.get('href')
        response = requests.put(href, data=open(file_path, 'rb'))

with open('token.txt', 'r') as file_object:
    token = file_object.read().strip()
file_object.close()

tokenYA =''
user = input('Введите id пользователя: ')
try:
    with open('token_Yandex.txt', 'r') as file_object:
        tokenYA = file_object.read().strip()
        file_object.close()
except FileNotFoundError:
    tokenYA= input('Введите токен Яндекс: ')


# проверяем возможность доступа к пользователю
URL = 'https://api.vk.com/method/users.get'
params = {
    'user_ids': user,
    'access_token': token, # токен и версия api являются обязательными параметрами во всех запросах к vk
    'v':'5.131',
    'fields': 'education,sex'
}
res = requests.get(URL, params=params).json()
flag = True

if res['response'][0]['can_access_closed']==False or res['response'][0]['first_name'] == 'DELETED':
    flag = False

#ищем фото
URL = 'https://api.vk.com/method/photos.get'
params = {
    'owner_id': user,
    'album_id': 'wall',
    'extended': '1',
    'photo_sizes': '1',
    'access_token': token, # токен и версия api являются обязательными параметрами во всех запросах к vk
    'v':'5.131',
    'fields': 'education,sex'
}
res1 = requests.get(URL, params=params).json()
uploader = YaUploader(tokenYA)
if flag:
    num = min(res1['response']['count'], 5)
    files = []
    file = {
   }
    #bar = range(num)
    #print('bar= ', bar)

    for item in range(num):
        file = {
        }



        print(f"Загрузка изображения {item+1} из {num} изображений")
        #bar.next()
        #time.sleep(1)
        files_url = res1['response']['items'][item]['sizes'][-1]['url']
        date = res1['response']['items'][0]['date']
        date_time = datetime.datetime.fromtimestamp(date)
        date_time = date_time.strftime('%Y-%m-%d')
        date_str = ''.join(str(date_time))+str(item)+'.jpg'
        count = res1['response']['items'][0]['likes']['count']
        if count !=0:
            date_str = str(count)+str(item)+'.jpg'

        response = requests.get(files_url)
        out = open(date_str, "wb")
        out.write(response.content)
        out.close()
        file["file_name"] = date_str
        file["size"] = res1['response']['items'][item]['sizes'][-1]['type']
        files.append(file)

        result = uploader.upload(date_str)
    bar.finish()
    with open('out.json', "w") as out:
        json.dump({"channel": files}, out, ensure_ascii=False, indent=2)
        out.close()
else:
    print('нет доступа к пользователю')





