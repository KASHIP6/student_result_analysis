import sqlite3
import pandas as pd

def fetch_data(query):
    """
    Fetch data from the SQLite database.
    """
    conn = sqlite3.connect('student_results.db')
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def calculate_pass_fail(marks, passing_marks=40):
    """
    Calculate pass/fail status based on marks.
    """
    return 'Pass' if marks >= passing_marks else 'Fail'

def get_top_students(df, n=5):
    """
    Get the top N students based on marks.
    """
    return df.nlargest(n, 'marks')

def get_failures(df):
    """
    Get the list of students who failed.
    """
    return df[df['marks'] < 40]

def generate_report(df):
    """
    Generate a report with average marks and attendance for each student.
    """
    report = df.groupby('name').agg({'marks': 'mean', 'attendance': 'mean'}).reset_index()
    return report