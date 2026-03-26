from requests import get, post, delete, put

#Получение работ
print(get('http://127.0.0.1:5000/api/jobs').json())

print(get('http://127.0.0.1:5000/api/jobs/1').json())

print(get('http://127.0.0.1:5000/api/jobs/45').json())

print(get('http://127.0.0.1:5000/api/jobs/q').json())




#Добавление работы
print(get('http://127.0.0.1:5000/api/jobs').json()) #Начальный список работ

print(post('http://127.0.0.1:5000/api/jobs', json={}).json()) #Пустой JSON. Данных для передачи нет

print(post('http://127.0.0.1:5000/api/jobs', #Переданы не все параметры для добавления работы
           json={'job': 'Заголовок'}).json())

print(post('http://127.0.0.1:5000/api/jobs', #Вместо булевого значения передана строка
           json={'job': 'running',
                 'team_leader': '3',
                 'work_size': 23,
                 'is_finished': 'False',
                 'collaborators': '1, 2'}).json())

print(post('http://127.0.0.1:5000/api/jobs',
           json={'job': 'running',
                 'team_leader': '3',
                 'work_size': 23,
                 'is_finished': False,
                 'collaborators': '1, 2'}).json())

print(get('http://127.0.0.1:5000/api/jobs').json()) #Список работ после добавления





#Удаление работы
print(delete('http://127.0.0.1:5000/api/jobs/12').json())

print(delete('http://127.0.0.1:5000/api/jobs/89').json())

print(delete('http://127.0.0.1:5000/api/jobs/hd').json())

print(get('http://127.0.0.1:5000/api/jobs').json())





#Редактирование работы
print(get('http://127.0.0.1:5000/api/jobs.20').json()) #работа до редактирования

print(put('http://127.0.0.1:5000/api/jobs/20',
           json={'job': 'cooking',
                 'team_leader': '3',
                 'work_size': 15,
                 'is_finished': False,
                 'collaborators': '1, 2'}).json())

print(put('http://127.0.0.1:5000/api/jobs/20', json={}).json()) #Пустой JSON.

print(put('http://127.0.0.1:5000/api/jobs/20', #Переданы не все параметры для изменения работы
           json={'job': 'Заголовок'}).json())

print(put('http://127.0.0.1:5000/api/jobs/20', #Вместо булевого значения передана строка
           json={'job': 'running',
                 'team_leader': '3',
                 'work_size': 23,
                 'is_finished': 'False',
                 'collaborators': '1, 2'}).json())



print(get('http://127.0.0.1:5000/api/jobs.20').json()) #работа после редактирования






#Действия с пользователями
print(get('http://127.0.0.1:5000/api/v2/users').json()) #Все пользователи

print(get('http://127.0.0.1:5000/api/v2/users/1').json()) #По id
print(get('http://127.0.0.1:5000/api/v2/users/999').json()) #Несуществующий id

new_user = {  #Добавление пользователя
    'surname': 'Ivanov',
    'name': 'Ivan',
    'age': 25,
    'position': 'engineer',
    'speciality': 'programmer',
    'address': 'module_2',
    'email': 'ivan@example.com',
    'password': 'secret123'
}
print(post('http://127.0.0.1:5000/api/v2/users', json=new_user).json())

new_user = {  #Неверный параметр
    'surname': 'Ivanov',
    'name': 'Ivan',
    'age': 'jfhgfjhg',
    'position': 'engineer',
    'speciality': 'programmer',
    'address': 'module_2',
    'email': 'ivan@example.com',
    'password': 'secret123'
}
print(post('http://127.0.0.1:5000/api/v2/users', json=new_user).json())

new_user = {  #Отсутствующий параметр
    'name': 'Ivan',
    'age': 25,
    'position': 'engineer',
    'speciality': 'programmer',
    'address': 'module_2',
    'email': 'ivan@example.com',
    'password': 'secret123'
}
print(post('http://127.0.0.1:5000/api/v2/users', json=new_user).json())

edit_user = {  #Изменения данных пользователя
    'surname': 'Mironov',
    'name': 'Miron',
    'age': 25,
    'position': 'engineer',
    'speciality': 'programmer',
    'address': 'module_2',
    'email': 'ivan@example.com',
    'password': 'secret123'
}
print(put('http://127.0.0.1:5000/api/v2/users/6', json=edit_user).json())

print(delete('http://127.0.0.1:5000/api/v2/users/6').json()) #Удаление пользователя





#Действия с работами
print(get('http://127.0.0.1:5000/api/v2/jobs').json()) #Все работы

print(get('http://127.0.0.1:5000/api/v2/jobs/1').json()) #По id
print(get('http://127.0.0.1:5000/api/v2/jobs/999').json()) #Несуществующий id

new_job = {    #добавление работы
    'job': 'playing',
    'team_leader': '1',
    'work_size': 6,
    'collaborators': '2, 3',
    'is_finished': False,
}
print(post('http://127.0.0.1:5000/api/v2/jobs', json=new_job).json())

new_job = {    #Неверный параметр
    'job': 'playing',
    'team_leader': '1',
    'work_size': 'fgdhgfh',
    'collaborators': '2, 3',
    'is_finished': False,
}
print(post('http://127.0.0.1:5000/api/v2/jobs', json=new_job).json())

new_job = {   #Отсутствующий параметр
    'team_leader': '1',
    'work_size': 4,
    'collaborators': '2, 3',
    'is_finished': False,
}
print(post('http://127.0.0.1:5000/api/v2/jobs', json=new_job).json())

edit_job = {   #Изменение работы
    'job': 'playing',
    'team_leader': '1',
    'work_size': 4,
    'collaborators': '2, 3',
    'is_finished': False,
}
print(put('http://127.0.0.1:5000/api/v2/jobs/17', json=edit_job).json())

print(delete('http://127.0.0.1:5000/api/v2/jobs/17').json()) #Удаление работы