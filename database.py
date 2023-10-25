import mysql.connector

database = mysql.connector.connect(
    host='HOST',
    user='USER',
    password='PASSWORD',
    database='DB'
)