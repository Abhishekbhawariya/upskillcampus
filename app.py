import sqlite3
from datetime import date
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
DB_NAME = "library.db"


def connect_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def create_tables():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            quantity INTEGER NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS members (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS issued_books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_id INTEGER,
            member_id INTEGER,
            issue_date TEXT,
            return_date TEXT,
            status TEXT DEFAULT 'Issued',
            FOREIGN KEY(book_id) REFERENCES books(id),
            FOREIGN KEY(member_id) REFERENCES members(id)
        )
    """)

    conn.commit()
    conn.close()


@app.route("/")
def index():
    return render_template("index.html")


# ---------------- API ENDPOINTS ----------------

@app.route("/api/stats", methods=["GET"])
def get_stats():
    conn = connect_db()
    cursor = conn.cursor()

    total_books = cursor.execute("SELECT IFNULL(SUM(quantity), 0) FROM books").fetchone()[0]
    total_titles = cursor.execute("SELECT COUNT(*) FROM books").fetchone()[0]
    total_members = cursor.execute("SELECT COUNT(*) FROM members").fetchone()[0]
    active_issued = cursor.execute("SELECT COUNT(*) FROM issued_books WHERE status = 'Issued'").fetchone()[0]

    conn.close()
    return jsonify({
        "total_books": total_books,
        "total_titles": total_titles,
        "total_members": total_members,
        "active_issued": active_issued
    })


@app.route("/api/books", methods=["GET", "POST"])
def manage_books():
    conn = connect_db()
    cursor = conn.cursor()

    if request.method == "POST":
        data = request.get_json()
        title = data.get("title", "").strip()
        author = data.get("author", "").strip()
        quantity = int(data.get("quantity", 0))

        if not title or not author or quantity < 1:
            return jsonify({"error": "Invalid book details"}), 400

        cursor.execute(
            "INSERT INTO books (title, author, quantity) VALUES (?, ?, ?)",
            (title, author, quantity)
        )
        conn.commit()
        conn.close()
        return jsonify({"message": "Book added successfully!"}), 201

    # GET books
    search = request.args.get("search", "").strip()
    if search:
        cursor.execute("SELECT * FROM books WHERE title LIKE ? OR author LIKE ?", (f"%{search}%", f"%{search}%"))
    else:
        cursor.execute("SELECT * FROM books ORDER BY id DESC")
    books = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify(books)


@app.route("/api/members", methods=["GET", "POST"])
def manage_members():
    conn = connect_db()
    cursor = conn.cursor()

    if request.method == "POST":
        data = request.get_json()
        name = data.get("name", "").strip()
        phone = data.get("phone", "").strip()

        if not name or not phone:
            return jsonify({"error": "Name and phone number are required"}), 400

        cursor.execute(
            "INSERT INTO members (name, phone) VALUES (?, ?)",
            (name, phone)
        )
        conn.commit()
        conn.close()
        return jsonify({"message": "Member added successfully!"}), 201

    cursor.execute("SELECT * FROM members ORDER BY id DESC")
    members = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify(members)


@app.route("/api/issue", methods=["POST"])
def issue_book_api():
    data = request.get_json()
    book_id = data.get("book_id")
    member_id = data.get("member_id")

    conn = connect_db()
    cursor = conn.cursor()

    # Verify Book
    cursor.execute("SELECT quantity FROM books WHERE id = ?", (book_id,))
    book = cursor.fetchone()
    if not book:
        conn.close()
        return jsonify({"error": "Book not found"}), 404
    if book["quantity"] <= 0:
        conn.close()
        return jsonify({"error": "Book is currently out of stock"}), 400

    # Verify Member
    cursor.execute("SELECT id FROM members WHERE id = ?", (member_id,))
    if not cursor.fetchone():
        conn.close()
        return jsonify({"error": "Member not found"}), 404

    # Issue book & decrement quantity
    cursor.execute("""
        INSERT INTO issued_books (book_id, member_id, issue_date, status)
        VALUES (?, ?, ?, 'Issued')
    """, (book_id, member_id, str(date.today())))

    cursor.execute("UPDATE books SET quantity = quantity - 1 WHERE id = ?", (book_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Book issued successfully!"})


@app.route("/api/return/<int:issue_id>", methods=["POST"])
def return_book_api(issue_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT book_id, status FROM issued_books WHERE id = ?", (issue_id,))
    issue = cursor.fetchone()

    if not issue:
        conn.close()
        return jsonify({"error": "Issue record not found"}), 404

    if issue["status"] == "Returned":
        conn.close()
        return jsonify({"error": "Book has already been returned"}), 400

    book_id = issue["book_id"]

    cursor.execute("""
        UPDATE issued_books
        SET return_date = ?, status = 'Returned'
        WHERE id = ?
    """, (str(date.today()), issue_id))

    cursor.execute("UPDATE books SET quantity = quantity + 1 WHERE id = ?", (book_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Book returned successfully!"})


@app.route("/api/issued", methods=["GET"])
def get_issued_books():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            issued_books.id,
            issued_books.book_id,
            books.title AS book_title,
            issued_books.member_id,
            members.name AS member_name,
            issued_books.issue_date,
            issued_books.return_date,
            issued_books.status
        FROM issued_books
        JOIN books ON issued_books.book_id = books.id
        JOIN members ON issued_books.member_id = members.id
        ORDER BY issued_books.id DESC
    """)
    records = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify(records)


if __name__ == "__main__":
    create_tables()
    print("🚀 Server running on http://127.0.0.1:5000")
    app.run(debug=True)