#курсовая работа

import configparser
import vk



if __name__ == "__main__":
    tokenYA =''
    user = input('Введите id пользователя или screen_name: ')
    num_foto = int(input('Введите кол-во скачиваемых фото: '))

    config = configparser.ConfigParser()  # создаём объекта парсера
    config.read("settings.ini")  # читаем конфиг

    token = config["Токены"]["token"]
    tokenYA = config["Токены"]["tokenYA"]

    VK_photo = vk.VKPhoto(token)
    result = VK_photo.searchphoto(token, tokenYA, user, num_foto)





