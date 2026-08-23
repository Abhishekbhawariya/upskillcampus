# 📚 Library Management System

A full-featured, lightweight **Library Management System** built with **Python** and **SQLite3**. It supports three interface modes: a modern **Web Dashboard (Flask + CSS)**, a standalone **Desktop GUI (Tkinter)**, and a **Command Line Interface (CLI)**.

---

## 🌟 Key Features

- 📖 **Book Management**: Add books, browse catalog, search by title/author, and monitor available stock in real-time.
- 👥 **Member Management**: Register library members with contact details and maintain a member directory.
- 🔄 **Book Issuing & Returning**:
  - Issue books to members with automated stock deduction.
  - Return books with timestamp tracking and automatic inventory replenishment.
  - Prevents borrowing out-of-stock books or non-existent IDs.
- 📊 **Live Analytics Dashboard**: View total book inventory, unique titles, registered members, and active borrows.
- 🎨 **Modern Responsive UI**: Custom CSS theme with glassmorphism touches, status badges, and mobile responsiveness.

---

## 🛠️ Tech Stack

| Component | Technologies Used |
| :--- | :--- |
| **Backend** | Python 3, Flask |
| **Database** | SQLite3 |
| **Frontend** | HTML5, CSS3 (`style.css`), JavaScript, Bootstrap 5, FontAwesome |
| **Desktop GUI** | Python Tkinter & ttk |

---

## 📁 Project Structure

```text
library-management-system/
│
├── app.py                  # Flask Web Server & REST API
├── desktop_app.py          # Tkinter Desktop GUI Application
├── cli_app.py              # Terminal Command Line Interface
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
│
├── static/
│   └── style.css           # Custom modern stylesheet
│
└── templates/
    └── index.html          # Web Dashboard UI template