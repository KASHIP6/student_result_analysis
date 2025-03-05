import sqlite3
import pandas as pd

def create_database():
    # Connect to SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect('student_results.db')
    cursor = conn.cursor()

    # Create a table for student results
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            subject TEXT NOT NULL,
            marks INTEGER NOT NULL,
            attendance INTEGER NOT NULL
        )
    ''')

    # Commit changes and close the connection
    conn.commit()
    conn.close()

def load_data_from_excel(file_path):
    # Load data from Excel
    df = pd.read_excel(file_path)

    # Connect to SQLite database
    conn = sqlite3.connect('student_results.db')
    cursor = conn.cursor()

    # Insert data into the database
    for _, row in df.iterrows():
        cursor.execute('''
            INSERT INTO students (name, subject, marks, attendance)
            VALUES (?, ?, ?, ?)
        ''', (row['Name'], row['Subject'], row['Marks'], row['Attendance']))

    # Commit changes and close the connection
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_database()
    load_data_from_excel('data/student_results_55.xlsx')
