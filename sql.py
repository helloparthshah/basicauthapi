import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="test",
    password="password",
    database="test"
)

mycursor = mydb.cursor()

mycursor.execute("SHOW DATABASES")

for x in mycursor:
    print(x)
