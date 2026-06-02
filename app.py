# First, we are importing  the tools we are going to use from Flask.
# 'Flask' is the app itself.
# 'jsonify' turns our Python dictionaries into JSON (the universal language of APIs).
# 'request' lets us look at the data the user is sending to us.
import sqlite3
from flask import Flask, jsonify, request

# Here, we are creating our actual app. 
# __name__ is just a special Python variable that tells Flask where to look for files
app = Flask(__name__)

# This is the name of the file where the database will save everything.
# Python will create this file automatically in the project folder!
DATABASE_FILE = "bookshelf.db"

# DATABASE setup funktion
# 
def initialize_database():
    connection = sqlite3.connect(DATABASE_FILE) # connection to the database
    cursor = connection.cursor() # creating a cursor that will execute SQL commands
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            author TEXT,
            genre TEXT
        )
        """
    )  # creating the tabele

    cursor.execute("SELECT COUNT(*) FROM books")  # adding some starter data, only if the database is already empty
    if (
        cursor.fetchone()[0] == 0
    ):  # it the count of rows is 0 add starater books
        cursor.execute(
            """
            INSERT INTO books (title, author, genre) VALUES
                ('The Hobbit', 'JRR Tolkien', 'Fantasy'),
                ('The Lord of the Rings', 'JRR Tolkien', 'Fantasy'),
                ('1984', 'George Orwell', 'Dystopian'),
                ('The Catcher in the Rye', 'J.D Salinger', 'Coming of Age'),
                ('To Kill a Mockingbird', 'Harper Lee', 'Classic'),
                ('The Great Gatsby', 'F. Scott Fitzgerald', 'Classic'),
                ('Pride and Prejudice', 'Jane Austen', 'Romance')
            """
        )
        # Whenever we CHANGE data (insert, update, delete), we MUST commit it.
        # connection.commit() is like hitting 'Ctrl + S' to save a file
        connection.commit()  

    connection.close()  # closing the connection


initialize_database()

# ENDPOINT !: GET ALL BOOKS
@app.route("/books", methods=["GET"])  # decorator
def get_all_books():
    #  opening the database conection
    connection = sqlite3.connect(DATABASE_FILE)
    cursor = connection.cursor()  # creating a cursor that will execute SQL commands

    # asking the database to give us everythign from the books table
    cursor.execute("SELECT id, title, author, genre FROM books")
    all_rows = cursor.fetchall()  # this grabs all the results as a list of tuples

    # close the database connection
    connection.close()

    # the API needs a JSON formating so we need to conwert the raw data to JSON

    formated_books = []  #  creating an empty list
    for row in all_rows:
        book_dictionary = {
            "id": row[0],   # row[0] means the first column
            "title": row[1],  # row[1] means the second column
            "author": row[2],  # row[2] means the third column
        }
        formated_books.append(book_dictionary)  # adding the dictionary to the list

    # Send the clean list back to the user
    return jsonify(formated_books)

#  ENDPOINT 2: GETING A SPECIFIC BOOK
@app.route("/books/<int:book_id>", methods=["GET"])
def get_one_book(book_id):
    connection = sqlite3.connect(DATABASE_FILE)  # opening the database connectioon
    cursor = connection.cursor()  # creating a cursor that will execute SQL commands

    # '?' as a placeholder for safety. This prevents a type of hacking called "SQL Injection".
    # We pass the real 'book_id' inside a tuple at the end: (book_id,)

    cursor.execute(
        "SELECT id, title, author, genre FROM books WHERE id = ?", (book_id,)
    )
    single_row = (
        cursor.fetchone()  # fetchone() only  grabs ONE result instead of all of them
    )

    connection.close()

    # If the database found a matching book.....
    if single_row:
        book_dictionary = {
            "id": single_row[0],
            "title": single_row[1],
            "author": single_row[2],
            "genre": single_row[3],
        }
        return jsonify(book_dictionary)  # Send the clean dictionary back to the user

        # if singel_row is empty, it means the book dosent exist
    return jsonify({"error": "Book not found"}), 404

# ENDPOINT 3: ADD A NEW BOOK
@app.route("/books", methods=["POST"])
def add_book():
    user_data = request.get_json()
    connection = sqlite3.connect(DATABASE_FILE)
    cursor = connection.cursor()

    # Add genre placeholder to the SQL command
    cursor.execute(
        "INSERT INTO books (title, author, genre) VALUES (?, ?, ?)",
        (user_data["title"], user_data["author"], user_data["genre"]),
    )
    connection.commit()
    new_book_id = cursor.lastrowid
    connection.close()

    created_book = {
        "id": new_book_id,
        "title": user_data["title"],
        "author": user_data["author"],
        "genre": user_data["genre"]
    }
    return jsonify(created_book), 201



# RUNNING THE APP

if __name__ == "__main__":
    app.run(debug=True)


