
from flask import Flask, request, jsonify
import requests
from datetime import datetime
from config import token, url
from db_sql import NimbleDbSQL


app = Flask(__name__)

db = NimbleDbSQL()


@app.route('/api/search', methods=['GET'])
def search_contacts():
    query = request.args.get('query')
    print(f'query: {query}')
    if query:
        search_results = db.fulltext_search(query)
        return jsonify(search_results)
    else:
        return jsonify({'error': 'Missing query parameter'}), 400


# Метод для выполнения GET-запроса и обновления базы данных раз в сутки
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
    app.run(debug=True)
