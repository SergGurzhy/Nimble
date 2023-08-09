host = '127.0.0.1'
user = 'postgres'
password = 'qwerty'
db_name = 'nimble_db'


создание базы:  docker run --name nimble_db --env-file .env -p 5432:5432 -d postgres
