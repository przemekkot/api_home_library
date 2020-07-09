from flask import Flask, jsonify, abort, make_response, request
from models import home_library

app = Flask(__name__)
app.config["SECRET_KEY"] = "zyrafyidadoszafy"


@app.route("/api/v1/homelibrary/", methods=["GET"])
def books_api_v1():
    return jsonify(home_library.all())


@app.route("/api/v1/homelibrary/<int:book_id>", methods=["GET"])
def get_book(book_id):
    book = home_library.get(book_id)
    if not book:
        abort(404)
    return jsonify({"book": book})


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found', 'status_code': 404}), 404)


@app.route("/api/v1/homelibrary/", methods=["POST"])
def create_book():
    if not request.json or not 'title' in request.json:
        abort(400)
    book = {
        'book_id': len(home_library.all()),
        'title': request.json['title'],
        'author': request.json['author'],
        'description': request.json.get('description', ""),
        'read': False
    }
    home_library.create(book)
    return jsonify({'book': book}), 201


@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request', 'status_code': 400}), 400)


@app.route("/api/v1/homelibrary/<int:book_id>", methods=['DELETE'])
def delete_book(book_id):
    result = home_library.delete(book_id)
    if not result:
        abort(404)
    return jsonify({'result': result})


@app.route("/api/v1/homelibrary/<int:book_id>", methods=["PUT"])
def update_book(book_id):
    book = home_library.get(book_id)
    if not book:
        abort(404)
    if not request.json:
        abort(400)
    data = request.json
    if any([
        'title' in data and not isinstance(data.get('title'), str),
        'author' in data and not isinstance(data.get('author'), str),
        'description' in data and not isinstance(data.get('description'), str),
        'read' in data and not isinstance(data.get('read'), bool)
    ]):
        abort(400)
    book = {
        'book_id': data.get('book_id', book['book_id']),
        'title': data.get('title', book['title']),
        'author': data.get('author', book['author']),
        'description': data.get('description', book['description']),
        'read': data.get('read', book['read'])
    }
    home_library.update(book_id, book)
    return jsonify({'book': book})
    

if __name__ == "__main__":
    app.run(debug=True)

