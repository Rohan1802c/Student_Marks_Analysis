import sqlite3
import csv
import os
from visualization import visualization_menu

DB_FILE = "database.db"
CSV_FILE = "students.csv"


def csv_to_sqlite():
    """Convert CSV data to SQLite database."""
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)  # Remove existing database to recreate
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Create table
    cursor.execute("""
    CREATE TABLE students (
        RollNo INTEGER PRIMARY KEY,
        Name TEXT,
        Physics_Test1 INTEGER, Physics_Test2 INTEGER, Physics_Test3 INTEGER, Physics_Final INTEGER,
        Chemistry_Test1 INTEGER, Chemistry_Test2 INTEGER, Chemistry_Test3 INTEGER, Chemistry_Final INTEGER,
        Maths_Test1 INTEGER, Maths_Test2 INTEGER, Maths_Test3 INTEGER, Maths_Final INTEGER,
        Computer_Test1 INTEGER, Computer_Test2 INTEGER, Computer_Test3 INTEGER, Computer_Final INTEGER
    )
    """)

    # Insert data from CSV
    with open(CSV_FILE, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            cursor.execute("""
            INSERT INTO students VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                int(row['RollNo']), row['Name'],
                int(row['Physics_Test1']), int(row['Physics_Test2']), int(row['Physics_Test3']), int(row['Physics_Final']),
                int(row['Chemistry_Test1']), int(row['Chemistry_Test2']), int(row['Chemistry_Test3']), int(row['Chemistry_Final']),
                int(row['Maths_Test1']), int(row['Maths_Test2']), int(row['Maths_Test3']), int(row['Maths_Final']),
                int(row['Computer_Test1']), int(row['Computer_Test2']), int(row['Computer_Test3']), int(row['Computer_Final'])
            ))
    conn.commit()
    conn.close()
    print("CSV data successfully converted to SQLite database.")


def view_students():
    """Display all student records."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()
    conn.close()
    for row in rows:
        print(row)


def search_student():
    """Search student by roll number or name."""
    search_term = input("Enter Roll Number or Name to search: ")
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students WHERE RollNo = ? OR Name LIKE ?", (search_term, f"%{search_term}%"))
    rows = cursor.fetchall()
    conn.close()
    if rows:
        for row in rows:
            print(row)
    else:
        print("No records found.")


def update_student():
    """Update a student's record."""
    roll_no = input("Enter Roll Number of student to update: ")
    field = input("Enter field to update (e.g., Name, Physics_Test1): ")
    new_value = input("Enter new value: ")

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(f"UPDATE students SET {field} = ? WHERE RollNo = ?", (new_value, roll_no))
    conn.commit()
    conn.close()
    print("Record updated successfully.")


def delete_student():
    """Delete a student's record."""
    roll_no = input("Enter Roll Number of student to delete: ")
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM students WHERE RollNo = ?", (roll_no,))
    conn.commit()
    conn.close()
    print("Record deleted successfully.")


def main():
    csv_to_sqlite()
    while True:
        print("\nOptions:")
        print("1. View student records")
        print("2. Search student by roll number or name")
        print("3. Update student data")
        print("4. Delete student data")
        print("5. Generate visualizations")
        print("6. Exit")

        choice = input("Enter your choice: ")
        if choice == '1':
            view_students()
        elif choice == '2':
            search_student()
        elif choice == '3':
            update_student()
        elif choice == '4':
            delete_student()
        elif choice == '5':
            visualization_menu(DB_FILE)
        elif choice == '6':
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
