## Описание проекта

Представленный проект реализован в рамках тестового задания.

### Задание:
Написать API для просмотра и изменении информации о жильцах дома.
Реализовать endpoints для главной страницы с домом и его адресом, все CRUD операции для моделей 
Жильца, машины, парковочного места.

## Инструкция по установке и использованию API

##### Установите Docker или Docker-desktop, если он еще не установлен.

##### Клонируйте репозиторий в заранее созданную папку
```bash
cd <folder_name>
git clone https://github.com/Och1ta/test_br  
```

Запустите docker-compose с помощью команды:
```bash
docker-compose up --build 
```

Для выполнения миграций открыть второй терминал и выполнить команду:
```bash
docker-compose exec web python manage.py migrate
```

##### Для локального запуска 
Установить виртуальное окружение env
```bash
python -m venv venv
```
Установить зависимости с помощью:
```bash
pip install -r .\requirements.txt
```
Применить миграции
```bash
python manage.py migration
```
Запустить виртуальный сервер с помощью Uvicorn
```bash
python manage.py runserver
```

#### Пример env-файла
```bash
SECRET_KEY=''
DEBUG=True
ALLOWED_HOSTS='127.0.0.1, localhost'
DATABASES=postgres
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
```

### Проект выполнил [Кабанов Антон](https://github.com/Och1ta)