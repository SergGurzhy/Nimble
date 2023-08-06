from flask import Flask, request, jsonify
from db_factory import get_database

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


if __name__ == '__main__':
    app.run(debug=True)
