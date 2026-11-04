import os
import json

# считываем существующие данные или создаем пустой объект
FILE_NAME = "passwords.json"

if os.path.exists(FILE_NAME):
    with open(FILE_NAME, "r", encoding="utf-8") as f:
        passwords = json.load(f)
else:
    passwords = []
#########################################################

# авторизация


#########################################################


# логика


#########################################################


# entered_password = input("Введите пароль: ")
#
# if entered_password == password:
#     action = int(input("1 - посмотреть пароли, 2 - добавить пароль \n"))
#     if action == 1:
#         if len(passwords) > 0:
#             for password in passwords:
#                 print(*password)
#         else:
#             print("еще нет паролей")
#     elif action == 2:
#         new_service_name = input("Введите имя сервиса: ")
#         new_service_login = input("Введите логин от сервиса: ")
#         new_service_password = input("Введите пароль от сервиса: ")
#         passwords.append([new_service_name, new_service_login, new_service_password])
#         print(passwords)
# else:
#     print("неверный пароль")


# запись и сохранение данных - иначе изменения не сохранятся

with open(FILE_NAME, "w", encoding="utf-8") as f:
    json.dump(passwords, f, ensure_ascii=False, indent=4)

#########################################################