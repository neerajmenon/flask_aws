import sqlite3

connection = sqlite3.connect("user_data.db")
cursor = connection.cursor()
command = """CREATE TABLE IF NOT EXISTS users(name TEXT,password TEXT,email TEXT,firstname TEXT,lastname TEXT)"""
cursor.execute("INSERT INTO users VALUES('JoeRogan','42','jre@gmail.com','Joe','Rogan')")
connection.commit()    
