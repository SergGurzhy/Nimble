from flask import Flask, request, jsonify
import requests
from datetime import datetime
from config import token, url
from db_factory import get_database

app = Flask(__name__)

db = get_database()


@app.route('/api/search', methods=['GET'])
def search_contacts():
    query = request.args.get('query')
    print(f'query: {query}')
    if query:
        search_results = db.fulltext_search(query)
        return jsonify(search_results)
    else:
        return jsonify({'error': 'Missing query parameter'}), 400


@app.route('/api', methods=['GET'])
def get_all_records():
    # Получаем все записи из базы данных
    records = db.get_all_records()

    # Преобразовываем список объектов Person в список словарей
    data = [{'first_name': record.first_name, 'last_name': record.last_name, 'email': record.email} for record in
            records]

    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)
