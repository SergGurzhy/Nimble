import os
import sys
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from requests import RequestException
from db_factory import get_database
from server_helpers.db_service import ServiceDB
from server_helpers.helpers import update_db_daily


load_dotenv(sys.path[0] + '/.env')

app = Flask(__name__)
db = ServiceDB(get_database())


@app.route('/api/search', methods=['GET'])
def search_contacts():
    query = request.args.get('query')
    if query:
        search_results = db.full_text_search(query)
        return jsonify(search_results)
    else:
        return jsonify({'error': 'Missing query parameter'}), 400


@app.route('/api', methods=['GET'])
def get_all_records():
    return db.get_all_entries()


@app.route('/api/update', methods=['POST'])
def update_database():
    try:
        print(f'Token: {os.getenv("TOKEN")}')
        update_db_daily(db)
        return jsonify({'message': 'Database update successful'}), 200
    except RequestException as e:
        return jsonify({'error': f'An error occurred connecting to the server: {str(e)}'}), 500


@app.route('/api/drop', methods=['POST'])
def drop_table():
    try:
        db.drop_table()
        return jsonify({'message': 'Drop database successfully'}), 200
    except Exception as e:
        return jsonify({'error': f'An error occurred connecting to the server: {str(e)}'}), 500


if __name__ == '__main__':
    app.run(debug=True)
