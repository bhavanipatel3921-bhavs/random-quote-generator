from flask import Flask, render_template
import requests
import sqlite3

app = Flask(__name__)

# Create Database
def init_db():
    conn = sqlite3.connect('quotes.db')
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS quotes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        quote TEXT,
        author TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()


@app.route('/')
def home():

    try:
        api_url = "https://dummyjson.com/quotes/random"

        response = requests.get(api_url)

        data = response.json()

        quote = data['quote']
        author = data['author']

        # Save quote to database
        conn = sqlite3.connect('quotes.db')
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO quotes (quote, author) VALUES (?, ?)",
            (quote, author)
        )

        conn.commit()
        conn.close()

    except Exception as e:
        quote = "Unable to fetch quote."
        author = str(e)

    return render_template(
        'index.html',
        quote=quote,
        author=author
    )


@app.route('/history')
def history():

    conn = sqlite3.connect('quotes.db')
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM quotes ORDER BY id DESC"
    )

    quotes = cursor.fetchall()

    conn.close()

    return render_template(
        'history.html',
        quotes=quotes
    )


if __name__ == "__main__":
    app.run(debug=True)