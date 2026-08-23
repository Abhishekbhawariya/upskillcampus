📚 Library Management System
A library management application built with Python, SQLite Database, and a simple user-friendly interface for managing books, members, issue/return transactions, and book availability.
🌟 Features
📖 Book Management: Add new books, view existing books, search books, and update book information.
👨‍🎓 Member Management: Maintain student/member records including name, course, and contact details.
🔎 Book Search: Quickly search for books using book title or ID and check their availability.
📤 Book Issue: Issue an available book to a registered member and automatically update the available quantity.
📥 Book Return: Record returned books and automatically increase their available quantity.
📊 Availability Tracking: Track total and currently available copies of books.
💾 SQLite Database Persistence: Stores books, members, and issue/return transaction records in a SQLite database.
🛡️ Input Validation: Handles incorrect or empty inputs and prevents invalid database operations.
🗂️ Transaction Management: Maintains issue and return records with transaction ID, book ID, member ID, issue date, return date, and status.
📚 Library Modules
1. Book Management
Add new books
View books
Search books
Update book information
Track book quantity and availability
2. Member Management
Add and maintain member/student information
Store member ID, name, course, and contact details
3. Book Issue
Select an available book
Select a registered member
Create an issue transaction
Decrease available book quantity
4. Book Return
Select an issued transaction
Record the return
Increase available book quantity
Update transaction status
🗃️ Database Structure
Books Table
Field
Description
book_id
Primary Key
title
Book title
author
Book author
category
Book category
quantity
Total number of copies
available_quantity
Currently available copies
Members Table
Field
Description
member_id
Primary Key
name
Member/student name
course
Course name
contact
Contact information
Transactions Table
Field
Description
transaction_id
Primary Key
book_id
Issued book
member_id
Member who issued the book
issue_date
Issue date
return_date
Return date
status
Transaction status
🔄 Library Workflow
Start Application
       ↓
Select Operation
       ↓
Enter Required Details
       ↓
Validate Input
       ↓
Perform Database Operation
       ↓
Display Result
       ↓
Return to Main Menu / Exit
🛠️ Technologies Used
🐍 Python 3.x — Application development
🗄️ SQLite — Relational database
💻 VS Code / PyCharm / IDLE — Development environment
🖥️ Windows / Linux / macOS — Supported operating systems
📁 Project Structure
library-management/
├── app.py                  # Python application
├── library.db              # SQLite database
├── README.md               # Project documentation
├── templates/
│   └── index.html          # Main user interface
└── static/
    ├── style.css           # Application styling
    └── app.js              # Frontend JavaScript
Note: The first report specifically establishes Python + SQLite and the library modules; it does not establish that the original project actually contains Flask, HTML, CSS, JavaScript, or the exact file structure above. � �
BTU_Industrial_Internship_Report_Library_Management_System.docx
BTU_Industrial_Internship_Report_Library_Management_System.docx
🚀 Quick Start Guide
Prerequisites
Make sure Python 3.x is installed on your system.
1. Install / Verify Python
python --version
2. Run the Application
Navigate to the project folder and run:
python app.py
The exact filename of the Python entry point is not specified in the source report, so use the actual filename of your implementation. �
BTU_Industrial_Internship_Report_Library_Management_System.docx
3. Use the Application
From the main menu, perform operations such as:
Add Book
View Books
Search Book
Issue Book
Return Book
Manage Members
Check Availability
🔌 Application Operations
Operation
Description
Add Book
Adds a new book record
View Books
Displays stored books
Search Book
Searches by title/ID
Issue Book
Creates an issue transaction
Return Book
Records a book return
Member Management
Maintains member information
Availability
Tracks available copies
The source report confirms these as the core functional modules. �
BTU_Industrial_Internship_Report_Library_Management_System.docx
🧪 Testing
The system was tested for major operations:
Test Case
Expected Result
Status
Add Book
Book record is stored
Pass
Search Book
Matching record displayed
Pass
Issue Book
Transaction created and availability updated
Pass
Return Book
Return recorded and availability updated
Pass
Invalid Input
Validation message displayed
Pass
These test outcomes are taken directly from the Library Management System report. �
BTU_Industrial_Internship_Report_Library_Management_System.docx
🚀 Future Scope
The Library Management System can be enhanced with:
🌐 Web-based version using Flask or Django
🔐 Secure user authentication and role-based access
📱 Mobile application
📷 Barcode/QR-code scanning
💰 Automatic fine calculation
📧 Email/SMS due-date notifications
📊 Advanced reports and dashboards
☁️ MySQL/PostgreSQL and larger-scale deployment
These future enhancements are specifically listed in the source report. �
BTU_Industrial_Internship_Report_Library_Management_System.docx
📄 License
Created for the Library Management System – Industrial Internship Project.
Project: Library Management System
Student: Abhishek Bhawariya
University: Bikaner Technical University
Internship Duration: 4 Weeks
