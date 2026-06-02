#My REST API: The Virtual Bookshelf 

Hey there! This is a project I built to practice on how backend web development and databases actually work. It’s a simple **Virtual Bookshelf API** built completely in **Python** using **Flask** and a local **SQLite** database. 

I wanted to move past temporary data structures and learn how to actually save data permanently on a computer, and this is the result!

-------------------------

##What Does This Actually Do?
* **Remembers everything:** It uses a real SQLite database file (`bookshelf.db`). If I shut down the server or reboot my computer, my books don't vanish.
* **Sets itself up:** The first time it runs, it automatically creates a table and seeds it with 7 classic books so it’s not just a blank screen.
* **Speaks standard JSON:** It communicates using standard JSON formatting, making it ready to connect to a frontend website later.

--------------------------

## How To Get This Running

First, make sure you have Python installed. Then, grab Flask using your terminal:

```bash
pip install Flask

-To boot up the local server, run the python script:
python app.py
-Look for the line that says * Running on http://127.0.0.1:5000/. 
That means the server is live and waiting for requests!

Since this is a backend API, it doesn't have buttons or images. I use a web browser to read data, or tools like Postman to send new data.

1. Look at the whole shelf
URL: http://127.0.0.1:5000/books

Method: GET

What happens: It reads the database and spits out a clean list of every book I have stored, complete with titles, authors, and genres.

2. Grab a single book
URL: http://127.0.0.1:5000/books/<id_number> (Example: http://127.0.0.1:5000/books/3)

Method: GET

What happens: It looks up that exact ID. If the book exists, it displays it. If I type an ID that isn't real (like book 99), it sends back a custom 404 Book not found error message.

3. Add a new book to the shelf
URL: http://127.0.0.1:5000/books

Method: POST

What happens: It takes a JSON package containing a new book, saves it permanently to the database, generates a fresh ID for it, and returns the newly saved book as confirmation.

Example data package to send:
{
  "title": "The Alchemist",
  "author": "Paulo Coelho",
  "genre": "Adventure"
}

--------------------------


Behind the scenes, SQLite creates a local file called bookshelf.db. It has a single table called books structured like this:

id: A number that automatically counts up by itself (1, 2, 3...) so every book has a unique tracking number.

title: The text field for the book's title.

author: The text field for the writer.

genre: The text field to categorize the book.


  ===What I Learned Making This===
How to use Flask decorators (@app.route) to control web traffic.

The importance of clean Python indentation (a misplaced loop block can hide your data!).

How to safely use database placeholders (?) to prevent SQL injection vulnerabilities.