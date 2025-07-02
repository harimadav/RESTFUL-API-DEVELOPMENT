from flask import Flask, jsonify, request
import json

app = Flask(__name__)

# Load books from JSON
def load_books():
    with open('books.json', 'r') as f:
        return json.load(f)

# Save books to JSON
def save_books(books):
    with open('books.json', 'w') as f:
        json.dump(books, f, indent=4)

@app.route('/')
def home():
    return "Welcome to the Library API"

# GET all books
@app.route('/books', methods=['GET'])
def get_books():
    books = load_books()
    return jsonify(books)

# GET single book by ID
@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    books = load_books()
    book = next((b for b in books if b['id'] == book_id), None)
    if book:
        return jsonify(book)
    return jsonify({'message': 'Book not found'}), 404

# ADD new book
@app.route('/books', methods=['POST'])
def add_book():
    books = load_books()
    new_book = request.get_json()
    new_book['id'] = books[-1]['id'] + 1 if books else 1
    books.append(new_book)
    save_books(books)
    return jsonify(new_book), 201

# UPDATE book
@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    books = load_books()
    book = next((b for b in books if b['id'] == book_id), None)
    if not book:
        return jsonify({'message': 'Book not found'}), 404

    data = request.get_json()
    book.update(data)
    save_books(books)
    return jsonify(book)

# DELETE book
@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    books = load_books()
    updated_books = [b for b in books if b['id'] != book_id]
    if len(books) == len(updated_books):
        return jsonify({'message': 'Book not found'}), 404

    save_books(updated_books)
    return jsonify({'message': 'Book deleted'})

if __name__  ==  '__main__':
    app.run(debug=True)