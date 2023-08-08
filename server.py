from flask import Flask, request, jsonify
from db_factory import get_database
from server_helpers.helpers import update_db_daily

app = Flask(__name__)
db = get_database()


@app.route('/api/search', methods=['GET'])
def search_contacts():
    query = request.args.get('query')
    if query:
        search_results = db.fulltext_search(query)
        return jsonify(search_results)
    else:
        return jsonify({'error': 'Missing query parameter'}), 400


@app.route('/api', methods=['GET'])
def get_all_records():
    return db.get_all_records()


@app.route('/api/update', methods=['POST'])
def update_database():
    try:
        update_db_daily()
        return jsonify({'message': 'Database update successful'}), 200
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500


if __name__ == '__main__':
    app.run(debug=True)
