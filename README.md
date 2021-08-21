# final exam
Для запуска проекта установите python версии 3.7 и выше, pip и virualenv

Поссле клонирования перейдите в склонированную папку и вывполните следующие команды:

Создайте виртуальное окружение командой
```bash
python3 -m virtualenv -p python3 venv
```
либо
```bash
virtualenv -p python3 venv
```
Активируйте виртуальное окружение командой
```bash
source venv/bin/activate
```

Установите зависимости командой
```bash
pip install -r requirements.txt
```
Настройте конфигурацию данных PostgreSQL в `main/settings.py`
либо закомментируйте настройки базы postgres
```bash
DATABASES = {
    'default': {
        #
        'ENGINE': 'django.db.backends.postgresql',
        #
        'HOST': '127.0.0.1',
        'PORT': '5432',
        'NAME': 'attractor_db',
        'USER': 'attractor_user',
        'PASSWORD': 'attractor_pass',
    }
}
```
Примените миграции командой
```bash
python manage.py migrate
```

Загрузите фикстуры командой
```bash
python manage.py loaddata fixtures/dump.json
```
Для запуска сервера
```bash
python manage.py runserver
```

Данные для входа:
admin: admin  (superuser)
moder: moder (staff)
user1: user1 
user2: user2 
