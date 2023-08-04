import requests
from config import token, url
from db_sql import NimbleDbSQL
from datetime import datetime

db = NimbleDbSQL()


def update_db_daily():

    headers = {
        'Authorization': token
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        new_data = response.json()

        db.update_db(new_data)

        current_time = datetime.now().strftime('%Y-%m-%d %H:%M')
        print(f"База данных успешно обновлена. Время обновления: {current_time}")

    except Exception as e:
        print(f"Произошла ошибка при обновлении базы данных: {e}")


if __name__ == '__main__':
    update_db_daily()
