import os
import json

# структура хранения
# passwords = {
#     "apple": {
#         "login": "roman22@icloud.com",
#         "password": "qwerty1234"
#     }
# }

#########################################################

# авторизация

def unit_master(password):  # создать хэш мастера
    pass

def unlock(password):
    pass

#########################################################


# логика

def add_entry(name, login, pwd):
    pass

def list_entries() -> list[str]:
    pass

def get_entry(name): #-> login/pwd
    pass

def delete_entry(name):
    pass

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
