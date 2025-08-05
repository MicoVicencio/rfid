import sqlite3

def create_database():
    conn = sqlite3.connect("rfid.db")
    cursor = conn.cursor()

    # Create student table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS student (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        rfid TEXT UNIQUE NOT NULL,
        name TEXT NOT NULL,
        section TEXT NOT NULL,
        email TEXT,
        mobile TEXT
    )
    """)

    # Create parent table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS parent (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        rfid TEXT UNIQUE NOT NULL,
        name TEXT NOT NULL,
        child_rfid TEXT NOT NULL,
        email TEXT,
        mobile TEXT,
        FOREIGN KEY (child_rfid) REFERENCES student (rfid)
    )
    """)

    # Create logs table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_rfid TEXT NOT NULL,
        parent_rfid TEXT NOT NULL,
        timestamp TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()
    print("✅ rfid.db created with student, parent, and logs tables.")

# Run this once to initialize the database
if __name__ == "__main__":
    create_database()
