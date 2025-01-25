"""import json
import os

# Создаем заготовку для структуры ansible-playbook
playbook = {
    "name": "Deploy tasks",
    "hosts": "localhost",
    "tasks": []
}

# Функция для добавления задачи в playbook
def add_task(task):
    playbook["tasks"].append(task)

# Добавляем задачу: установка Python 3 с использованием Homebrew
add_task({
    "name": "Install python3 using Homebrew",
    "homebrew": {
        "name": "python",
        "state": "latest"
    }
})

# Добавляем задачу: установка pip-пакета beautifulsoup4
add_task({
    "name": "Install pip package beautifulsoup4",
    "pip": {
        "name": "beautifulsoup4",
        "state": "present"
    }
})

# Добавляем задачу: создание директории, если её нет
add_task({
    "name": "Ensure directory exists",
    "file": {
        "path": "./",
        "state": "directory"
    }
})

# Добавляем задачу: копирование файла exploit.py
add_task({
    "name": "Copy ../Ex00/exploit.py to ./exploit.py",
    "copy": {
        "src": "../Ex00/exploit.py",
        "dest": "./exploit.py"
    }
})

# Добавляем задачу: копирование файла evilcorp.html
add_task({
    "name": "Copy ../Ex00/evilcorp.html to ./evilcorp.html",
    "copy": {
        "src": "../Ex00/evilcorp.html",
        "dest": "./evilcorp.html"
    }
})

# Добавляем задачу: выполнение скрипта exploit.py
add_task({
    "name": "Execute ./exploit.py",
    "command": "python ./exploit.py",
    "register": "command_result",
    "failed_when": "command_result.rc != 0"
})

# Пишем playbook в файл deploy.yml
with open("deploy.yml", "w") as file:
    file.write("- " + json.dumps(playbook, indent=2).replace("\n", "\n  ") + "\n")

# Сообщаем пользователю, что файл успешно сгенерирован
print("Ansible playbook 'deploy.yml' успешно создан.")"""

import yaml
import os

# Создаем заготовку для структуры ansible-playbook
playbook = {
    "name": "Deploy tasks",
    "hosts": "localhost",
    "tasks": []
}

# Функция для добавления задачи в playbook
def add_task(task):
    playbook["tasks"].append(task)

# Добавляем задачу: установка Python 3 с использованием Homebrew
add_task({
    "name": "Install python3 using Homebrew",
    "homebrew": {
        "name": "python",
        "state": "latest"
    }
})

# Добавляем задачу: установка pip-пакета beautifulsoup4
add_task({
    "name": "Install pip package beautifulsoup4",
    "pip": {
        "name": "beautifulsoup4",
        "state": "present"
    }
})

# Добавляем задачу: создание директории, если её нет
add_task({
    "name": "Ensure directory exists",
    "file": {
        "path": "./",
        "state": "directory"
    }
})

# Добавляем задачу: копирование файла exploit.py
add_task({
    "name": "Copy ../Ex00/exploit.py to ./exploit.py",
    "copy": {
        "src": "../Ex00/exploit.py",
        "dest": "./exploit.py"
    }
})

# Добавляем задачу: копирование файла evilcorp.html
add_task({
    "name": "Copy ../Ex00/evilcorp.html to ./evilcorp.html",
    "copy": {
        "src": "../Ex00/evilcorp.html",
        "dest": "./evilcorp.html"
    }
})

# Добавляем задачу: выполнение скрипта exploit.py
add_task({
    "name": "Execute ./exploit.py",
    "command": "python ./exploit.py",
    "register": "command_result",
    "failed_when": "command_result.rc != 0"
})

# Пишем playbook в файл deploy.yml в формате YAML
with open("deploy.yml", "w") as file:
    yaml.dump([playbook], file, default_flow_style=False, allow_unicode=True)

# Сообщаем пользователю, что файл успешно сгенерирован
print("Ansible playbook 'deploy.yml' успешно создан.")