import os
import sys
from json import JSONDecodeError
import requests
from dotenv import load_dotenv
from requests import RequestException
from datetime import datetime
from db_factory import get_database

load_dotenv(sys.path[0] + '/.env')

db = get_database()
url = os.getenv('API_URL').lower().strip()
token = os.getenv('TOKEN').strip()

headers = {
    'Authorization': token
}


def update_db_daily():
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        new_data = response.json()

        db.update_db(new_data)

        current_time = datetime.now().strftime('%Y-%m-%d %H:%M')
        print(f"The database has been successfully updated. Update time: {current_time}")

    except RequestException as e:
        print(f"An error occurred connecting to the server: {e}")
        raise e
    except JSONDecodeError as e:
        print(f"The server returned an invalid response: {e}")
        raise e

#
# if __name__ == '__main__':
#     update_db_daily()
