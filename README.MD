# django_test
Тестовое задание "Решение задач на код" на Django + Vue.js

Как запустить backend
----------
1. Убедитесь, что docker-compose установлен
2. Выполните `docker-compose up`

После этого API станет доступно по адресу http://localhost:8000, админка — по http://localhost:8000/admin. 

По умолчанию у админа логин `admin`, пароль `12345678`.

Чтобы выполнить тесты, запустите `docker-compose up -d && docker-compose exec django python manage.py test && docker-compose stop`

Как запустить frontend
----------
1. Убедитесь, что node.js установлен
2. Перейдите в папку frontend (`cd ./frontend`)
3. Выполните `npm ci && npm run serve`

После этого интерфейс станет доступен по адресу http://localhost:8080

Использованные библиотеки и фреймворки
-----------------------------------
- Django
- Celery
- Vue.js
- TailwindCSS
