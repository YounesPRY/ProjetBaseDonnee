
import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="younes",
        password="yoyo1yo94@Pry",
        database="hotel_db"
    )

