import sqlite3

# Database setup
conn = sqlite3.connect("quiz_app.db")  # Create/Connect to the database
cursor = conn.cursor()

# Create necessary tables
cursor.execute("""
CREATE TABLE IF NOT EXISTS Users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question TEXT NOT NULL,
    option_a TEXT NOT NULL,
    option_b TEXT NOT NULL,
    option_c TEXT NOT NULL,
    option_d TEXT NOT NULL,
    correct_option TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Scores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    score INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES Users(id)
)
""")

conn.commit()


# Prepopulate DBMS questions
def populate_questions():
    """Add DBMS questions to the database if the Questions table is empty."""
    cursor.execute("SELECT COUNT(*) FROM Questions")
    if cursor.fetchone()[0] == 0: 
        dbms_questions = [
            ("Which of the following is a valid SQL statement to retrieve all rows from a table?",
             "SELECT * FROM table_name;", "GET ALL FROM table_name;", "FETCH * FROM table_name;", "EXTRACT * FROM table_name;", "A"),
            ("What does the term 'normalization' in DBMS refer to?",
             "Ensuring the database runs faster.", "Dividing the database into smaller tables and eliminating redundancy.",
             "Backing up the database.", "Adding more data to the database.", "B"),
            ("In an ER diagram, an entity set is represented by:",
             "Rectangle", "Ellipse", "Diamond", "Triangle", "A"),
            ("A transaction in DBMS must follow which set of properties?",
             "ACID (Atomicity, Consistency, Isolation, Durability)", "BASE (Basically Available, Soft State, Eventual Consistency)",
             "CRUD (Create, Read, Update, Delete)", "DML (Data Manipulation Language)", "A"),
            ("What is the primary purpose of an index in a database?",
             "To increase data redundancy.", "To speed up query processing.", "To secure the data.", "To store a backup of the data.", "B")
        ]

        for question in dbms_questions:
            cursor.execute("""
            INSERT INTO Questions (question, option_a, option_b, option_c, option_d, correct_option)
            VALUES (?, ?, ?, ?, ?, ?)
            """, question)

        conn.commit()
        print("DBMS questions added to the database.")


def register():
    """Register a new user."""
    username = input("Enter a username: ")
    password = input("Enter a password: ")

    try:
        cursor.execute("INSERT INTO Users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        print("Registration successful!")
    except sqlite3.IntegrityError:
        print("Username already exists. Please try a different one.")


def login():
    """Log in an existing user."""
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    cursor.execute("SELECT id FROM Users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()

    if user:
        print("Login successful!")
        return user[0]  
    else:
        print("Invalid credentials. Please try again.")
        return None


def attempt_quiz(user_id):
    """Allow the user to attempt the quiz."""
    cursor.execute("SELECT * FROM Questions")
    questions = cursor.fetchall()

    if not questions:
        print("No questions available in the database. Please contact the admin.")
        return

    score = 0

    for question in questions:
        print(f"\nQuestion: {question[1]}")
        print(f"A. {question[2]}")
        print(f"B. {question[3]}")
        print(f"C. {question[4]}")
        print(f"D. {question[5]}")

        answer = input("Enter your answer (A/B/C/D): ").upper()
        if answer == question[6]:
            score += 10  # Assume each question is worth 10 points

    print(f"\nYou scored: {score}")

    cursor.execute("INSERT INTO Scores (user_id, score) VALUES (?, ?)", (user_id, score))
    conn.commit()


def view_results(user_id):
    """View the user's quiz results."""
    cursor.execute("SELECT score FROM Scores WHERE user_id = ?", (user_id,))
    scores = cursor.fetchall()

    if scores:
        print("\nYour Scores:")
        for idx, score in enumerate(scores, 1):
            print(f"Attempt {idx}: {score[0]} points")
    else:
        print("\nNo scores found. You haven't attempted any quizzes yet.")

def main():
    populate_questions()  # Add DBMS questions to the database

    while True:
        print("\n--- Quiz App Menu ---")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            register()
        elif choice == "2":
            user_id = login()
            if user_id:
                while True:
                    print("\n--- User Menu ---")
                    print("1. Attempt Quiz")
                    print("2. View Results")
                    print("3. Logout")
                    user_choice = input("Enter your choice: ")

                    if user_choice == "1":
                        attempt_quiz(user_id)
                    elif user_choice == "2":
                        view_results(user_id)
                    elif user_choice == "3":
                        break
                    else:
                        print("Invalid choice. Please try again.")
        elif choice == "3":
            print("Thank you for using the Quiz App!")
            break
        else:
            print("Invalid choice. Please try again.")


# Run the program
if __name__ == "__main__":
    main()