import sqlite3

def get_connection():
    connection = sqlite3.connect("record.db")
    return connection
connection = get_connection()
cursor = connection.cursor()

cursor.execute("""
    CREATE UNIQUE INDEX IF NOT EXISTS
    idx_unique_acct_name
    ON accounts(acct_name)
""")

cursor.execute("""
    SELECT name
    FROM sqlite_master
    WHERE type = 'table'
    AND name NOT LIKE 'sqlite_%'
""")

tables = cursor.fetchall()

print("Your tables:")

for table in tables:
    print(table[0])

print(f"\nTotal tables: {len(tables)}")

connection.commit()
connection.close()