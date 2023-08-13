import sys
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from requests import RequestException
from db_factory import get_database
from server_helpers.db_service import ServiceDB
from server_helpers.helpers import update_db_daily

load_dotenv(sys.path[0] + '/.env')

app = Flask(__name__)
print('[INFO] Server start...')
db = ServiceDB(get_database())


@app.route('/api/search', methods=['GET'])
def full_text_search():
    query = request.args.get('query')
    if query:
        search_results = db.full_text_search(query)
        return jsonify(search_results)
    else:
        return jsonify({'error': 'Missing query parameter'}), 400


@app.route('/api', methods=['GET'])
def get_all_records():
    try:
        data = db.get_all_entries()
        return jsonify(data), 200
    except RequestException as e:
        return jsonify({'error': f'An error occurred connecting to the server: {str(e)}'}), 500


@app.route('/api/update', methods=['POST'])
def update_database():
    try:
        response = update_db_daily(db)
        if 'ERROR' not in response:
            return jsonify({'message': 'Database update successful'}), 200
        raise RequestException

    except RequestException as e:
        return jsonify({'error': f'An error occurred connecting to the server: {str(e)}'}), 500


@app.route('/api/drop', methods=['POST'])
def drop_table():
    try:
        db.drop_table()
        return jsonify({'message': 'Drop database successfully'}), 200
    except Exception as e:
        return jsonify({'error': f'An error occurred connecting to the server: {str(e)}'}), 500


@app.route('/api/initialization', methods=['POST'])
def initialisation_db():
    query = request.args.get('query').strip()
    try:
        db.initialisation_db(table_name=query)
        return jsonify({'message': 'DB initialisation successfully'}), 200
    except Exception as e:
        return jsonify({'error': f'An error occurred connecting to the DB: {str(e)}'}), 500


if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host='0.0.0.0', debug=True)
