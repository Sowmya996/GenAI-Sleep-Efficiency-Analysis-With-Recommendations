import sqlite3

DATABASE = "sleepwell.db"


def get_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def create_table():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sleep_reports (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            name TEXT,
            gender TEXT,
            age INTEGER,
            occupation TEXT,
            bmi TEXT,

            sleep_duration REAL,
            quality_sleep INTEGER,
            stress INTEGER,
            physical_activity REAL,

            blood_pressure TEXT,
            heart_rate INTEGER,
            daily_steps INTEGER,

            prediction TEXT
        )
    """)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_table()
    print("Database and sleep_reports table created successfully!")