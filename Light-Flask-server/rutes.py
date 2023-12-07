import pymysql
from flask import Flask, jsonify

app = Flask(__name__)

def get_db_connection():
    connection = pymysql.connect(host='your_host',
                                 user='your_user',
                                 password='your_password',
                                 db='your_dbname',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    return connection
