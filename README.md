Запуск докер контейнера
docker-compose up --build -d

Добавление данные для тестирования.
- docker-compose web exec python manage.py makemigrations
- docker-compose web exec python manage.py migrate
- docker-compose web exec python manage.py populate_test_data

- Эндпоинты для тестирования
- api/houses/<int:house_pk>/apartments/
- api/calculate-payment/<int:house_id>/
