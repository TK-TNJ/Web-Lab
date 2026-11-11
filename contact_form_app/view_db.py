import sqlite3

def view_database():
    conn = sqlite3.connect('contacts.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM contacts")
        rows = cursor.fetchall()

        if not rows:
            print("\n⚠️ The database is empty! Submit a contact form first.\n")
            return

        print("\n" + "=" * 80)
        print("📋 DATABASE CONTENTS (contacts.db)")
        print("=" * 80)

        for row in rows:
            print(f"ID:      {row['id']}")
            print(f"Name:    {row['name']}")
            print(f"Email:   {row['email']}")
            print(f"Phone:   {row['phone']}")
            print(f"Subject: {row['subject']}")
            print(f"Message: {row['message']}")
            print(f"Date:    {row['created_at']}")
            print("-" * 80)

    except sqlite3.OperationalError:
        print("\n❌ Table 'contacts' does not exist yet. Run app.py first!\n")

    finally:
        conn.close()

if __name__ == '__main__':
    view_database()