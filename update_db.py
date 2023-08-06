import os
import requests
from requests import RequestException
from datetime import datetime
from db_factory import get_database

db = get_database()


def update_db_daily():

    url = os.getenv('API_URL')
    token = os.getenv('TOKEN')

    headers = {
        'Authorization': token
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        new_data = response.json()

        db.update_db(new_data)

        current_time = datetime.now().strftime('%Y-%m-%d %H:%M')
        print(f"The database has been successfully updated. Update time: {current_time}")

    except RequestException as e:
        print(f"An error occurred while updating the database: {e}")


if __name__ == '__main__':
    update_db_daily()
