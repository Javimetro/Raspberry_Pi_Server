
from flask import request, jsonify
from project import app, db  # Import the Flask app and the SQLAlchemy instance
from project.models import Vote, Topic, ESPDevice, User   # Import your models

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


@app.route('/submit_vote', methods=['POST'])
def submit_vote():
    data = request.json
    vote_type = data.get("vote")
    topic_id = data.get("TopicID")

    if not vote_type or topic_id is None:
        return jsonify({'error': 'Missing vote type or topic ID'}), 400

    # Check if the topic exists
    topic = Topic.query.get(topic_id)
    if not topic:
        return jsonify({'error': 'Topic not found'}), 404

    # Create a new vote for the topic
    new_vote = Vote(VoteType=vote_type, TopicID=topic_id, VoteTime=datetime.utcnow())
    
    # Add the new vote to the session and commit the transaction
    db.session.add(new_vote)
    db.session.commit()

    return jsonify({'message': 'Vote submitted successfully'}), 201

if __name__ == '__main__':
    app.run(debug=True)


if __name__ == '__main__':
    app.run(debug=True)


