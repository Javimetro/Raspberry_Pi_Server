
import pymysql.cursors
from flask import Flask, jsonify, request, current_app

app = Flask(__name__)



# Function to open a new database connection
def get_db_connection():
    return pymysql.connect(host='localhost', #CHANGE FOR TESTING IN OWN PC
                           user='root',
                           password='Supervote50000',
                           db='votingsystem',
                           charset='utf8mb4', #This setting ensures that both the client and the server are communicating using the same character encoding
                           cursorclass=pymysql.cursors.DictCursor)

# Function to close an existing database connection
def close_db_connection(connection, cursor=None):
    if cursor:
        cursor.close()
    if connection:
        connection.close()

# Route for registering a device
def register_device():
    data = request.json
    if 'deviceID' not in data:
        return jsonify({'error': 'Missing deviceID'}), 400  # Bad Request for missing deviceID

    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        sql = "INSERT INTO ESPDevices (DeviceID) VALUES (%s)"
        cursor.execute(sql, (data['deviceID'],))
        connection.commit()
        return jsonify({'message': 'Device registered successfully!'}), 201
    except pymysql.MySQLError as e:
        current_app.logger.error(e)
        return jsonify({'error': 'Registration failed'}), 500
    finally:
        close_db_connection(connection, cursor)

if __name__ == '__main__':
    app.run(debug=True)
