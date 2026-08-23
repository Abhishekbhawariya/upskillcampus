import sqlite3
from datetime import date

DB_NAME = "library.db"


# ---------------- DATABASE ----------------

def connect_db():
    return sqlite3.connect(DB_NAME)


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


# ---------------- BOOK FUNCTIONS ----------------

def add_book():
    title = input("Enter book title: ")
    author = input("Enter author name: ")
    quantity = int(input("Enter quantity: "))

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO books (title, author, quantity) VALUES (?, ?, ?)",
        (title, author, quantity)
    )

    conn.commit()
    conn.close()

    print("Book added successfully!")


def view_books():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()

    conn.close()

    print("\n----- BOOK LIST -----")

    if not books:
        print("No books available.")
        return

    for book in books:
        print(
            f"ID: {book[0]} | "
            f"Title: {book[1]} | "
            f"Author: {book[2]} | "
            f"Quantity: {book[3]}"
        )


def search_book():
    keyword = input("Enter book title or author: ")

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM books
        WHERE title LIKE ? OR author LIKE ?
    """, (f"%{keyword}%", f"%{keyword}%"))

    books = cursor.fetchall()

    conn.close()

    print("\n----- SEARCH RESULT -----")

    if not books:
        print("Book not found.")
        return

    for book in books:
        print(
            f"ID: {book[0]} | "
            f"Title: {book[1]} | "
            f"Author: {book[2]} | "
            f"Quantity: {book[3]}"
        )


# ---------------- MEMBER FUNCTIONS ----------------

def add_member():
    name = input("Enter member name: ")
    phone = input("Enter phone number: ")

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO members (name, phone) VALUES (?, ?)",
        (name, phone)
    )

    conn.commit()
    conn.close()

    print("Member added successfully!")


def view_members():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM members")
    members = cursor.fetchall()

    conn.close()

    print("\n----- MEMBER LIST -----")

    if not members:
        print("No members found.")
        return

    for member in members:
        print(
            f"ID: {member[0]} | "
            f"Name: {member[1]} | "
            f"Phone: {member[2]}"
        )


# ---------------- ISSUE BOOK ----------------

def issue_book():
    book_id = int(input("Enter book ID: "))
    member_id = int(input("Enter member ID: "))

    conn = connect_db()
    cursor = conn.cursor()

    # Check book
    cursor.execute(
        "SELECT quantity FROM books WHERE id = ?",
        (book_id,)
    )

    book = cursor.fetchone()

    if book is None:
        print("Book not found.")
        conn.close()
        return

    if book[0] <= 0:
        print("Book is not available.")
        conn.close()
        return

    # Check member
    cursor.execute(
        "SELECT id FROM members WHERE id = ?",
        (member_id,)
    )

    member = cursor.fetchone()

    if member is None:
        print("Member not found.")
        conn.close()
        return

    # Issue book
    cursor.execute("""
        INSERT INTO issued_books
        (book_id, member_id, issue_date, status)
        VALUES (?, ?, ?, 'Issued')
    """, (book_id, member_id, str(date.today())))

    # Reduce quantity
    cursor.execute("""
        UPDATE books
        SET quantity = quantity - 1
        WHERE id = ?
    """, (book_id,))

    conn.commit()
    conn.close()

    print("Book issued successfully!")


# ---------------- RETURN BOOK ----------------

def return_book():
    issue_id = int(input("Enter issue ID: "))

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT book_id, status
        FROM issued_books
        WHERE id = ?
    """, (issue_id,))

    issue = cursor.fetchone()

    if issue is None:
        print("Issue record not found.")
        conn.close()
        return

    if issue[1] == "Returned":
        print("Book already returned.")
        conn.close()
        return

    book_id = issue[0]

    # Update issue record
    cursor.execute("""
        UPDATE issued_books
        SET return_date = ?, status = 'Returned'
        WHERE id = ?
    """, (str(date.today()), issue_id))

    # Increase book quantity
    cursor.execute("""
        UPDATE books
        SET quantity = quantity + 1
        WHERE id = ?
    """, (book_id,))

    conn.commit()
    conn.close()

    print("Book returned successfully!")


# ---------------- ISSUED BOOKS ----------------

def view_issued_books():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            issued_books.id,
            books.title,
            members.name,
            issued_books.issue_date,
            issued_books.return_date,
            issued_books.status
        FROM issued_books
        JOIN books ON issued_books.book_id = books.id
        JOIN members ON issued_books.member_id = members.id
    """)

    records = cursor.fetchall()

    conn.close()

    print("\n----- ISSUED BOOKS -----")

    if not records:
        print("No issue records found.")
        return

    for record in records:
        print(
            f"Issue ID: {record[0]} | "
            f"Book: {record[1]} | "
            f"Member: {record[2]} | "
            f"Issue Date: {record[3]} | "
            f"Return Date: {record[4]} | "
            f"Status: {record[5]}"
        )


# ---------------- MAIN MENU ----------------

def main():
    create_tables()

    while True:

        print("\n==============================")
        print("   LIBRARY MANAGEMENT SYSTEM")
        print("==============================")

        print("1. Add Book")
        print("2. View Books")
        print("3. Search Book")
        print("4. Add Member")
        print("5. View Members")
        print("6. Issue Book")
        print("7. Return Book")
        print("8. View Issued Books")
        print("9. Exit")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            add_book()

        elif choice == "2":
            view_books()

        elif choice == "3":
            search_book()

        elif choice == "4":
            add_member()

        elif choice == "5":
            view_members()

        elif choice == "6":
            issue_book()

        elif choice == "7":
            return_book()

        elif choice == "8":
            view_issued_books()

        elif choice == "9":
            print("Thank you!")
            break

        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()