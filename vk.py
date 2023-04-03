import requests
import tqdm
from tqdm import tqdm
from time import sleep
import json
import datetime


class YaUploader:
    def __init__(self, token: str):
        self.token = token

    def upload(self, file_path: str, photo: bytes):
        """Метод загружает файлы по списку file_list на яндекс диск"""


        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token),

        }
# создаем каталог для импорта и проверяем есть ли он

        files_url = 'https://cloud-api.yandex.net/v1/disk/resources'
        name_path = 'test_import'
        params = {'path': name_path}
        response = requests.put(files_url, headers=headers, params=params)
        files_url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        params = {'path': name_path+"/"+file_path, 'overwrite': 'true'}
        response = requests.get(files_url, headers=headers, params=params)
        data = response.json()
        href = data.get('href')
        response = requests.put(href, photo)

class VKPhoto:
    def __init__(self, token: str):
        self.token = token

    def searchphoto(self, token: str, tokenYA: str, user: int, num_foto: int):
        """Метод  ищет фото по списку file_list на яндекс диск"""
        # проверяем возможность доступа к пользователю
        URL = 'https://api.vk.com/method/users.get'
        params = {
            'user_ids': user,
            'access_token': token,  # токен и версия api являются обязательными параметрами во всех запросах к vk
            'v': '5.131',
            'fields': 'education, sex, screen_name'
        }
        res = requests.get(URL, params=params).json()
        user = res['response'][0]['id']
        # print(res)
        flag = True

        if res['response'][0]['can_access_closed'] == False or res['response'][0]['first_name'] == 'DELETED':
            flag = False

        # ищем фото
        URL = 'https://api.vk.com/method/photos.get'
        params = {
            'owner_id': user,
            'album_id': 'wall',
            'extended': '1',
            'photo_sizes': '1',
            'access_token': token,  # токен и версия api являются обязательными параметрами во всех запросах к vk
            'v': '5.131',
            'fields': 'education,sex'
        }
        res1 = requests.get(URL, params=params).json()

        uploader = YaUploader(tokenYA)
        if flag:
            num = min(res1['response']['count'], num_foto)
            files = []
            file = {
            }

            for item in tqdm(range(num), ncols=80, ascii=True, desc='Total'):
                sleep(0.1)
                file = {
                }

                # print(f"Загрузка изображения {item+1} из {num} изображений")

                files_url = res1['response']['items'][item]['sizes'][-1]['url']
                date = res1['response']['items'][0]['date']
                date_time = datetime.datetime.fromtimestamp(date)
                date_time = date_time.strftime('%Y-%m-%d')
                date_str = ''.join(str(date_time)) + str(item) + '.jpg'
                count = res1['response']['items'][0]['likes']['count']
                if count != 0:
                    date_str = str(count) + str(item) + '.jpg'

                response = requests.get(files_url)
                # out = open(date_str, "wb")
                # out.write(response.content)
                # out.close()
                file["file_name"] = date_str
                file["size"] = res1['response']['items'][item]['sizes'][-1]['type']
                files.append(file)

                # print(type(response.content))

                # result = uploader.upload(date_str)
                result = uploader.upload(date_str, response.content)
            with open('out.json', "w") as out:
                json.dump({"channel": files}, out, ensure_ascii=False, indent=2)
                out.close()
        else:
            print('нет доступа к пользователю')