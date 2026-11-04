password = "1"
passwords = [["apple", "roman22@icloud.com", "qwerty1234"],
             ["instagram", "roman234", "ytrewq4321"]
             ]

entered_password = input("Введите пароль: ")

if entered_password == password:
    action = int(input("1 - посмотреть пароли, 2 - добавить пароль \n"))
    if action == 1:
        if len(passwords) > 0:
            for password in passwords:
                print(*password)
        else:
            print("еще нет паролей")
    elif action == 2:
        new_service_name = input("Введите имя сервиса: ")
        new_service_login = input("Введите логин от сервиса: ")
        new_service_password = input("Введите пароль от сервиса: ")
        passwords.append([new_service_name, new_service_login, new_service_password])
        print(passwords)
else:
    print("неверный пароль")