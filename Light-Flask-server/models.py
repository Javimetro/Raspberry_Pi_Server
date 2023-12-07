from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class ESPDevice(db.Model):
    __tablename__ = 'ESPDevices'
    DeviceID = db.Column(db.String(17), primary_key=True)
    RegistrationTime = db.Column(db.DateTime, nullable=False)
    LastActiveTime = db.Column(db.DateTime, nullable=False)

class User(db.Model):
    __tablename__ = 'Users'
    UserID = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.String(80), unique=True, nullable=False)
    DeviceID = db.Column(db.String(17), db.ForeignKey('ESPDevices.DeviceID'))
    RegistrationDate = db.Column(db.DateTime, nullable=False)

class Topic(db.Model):
    __tablename__ = 'Topics'
    TopicID = db.Column(db.Integer, primary_key=True)
    Title = db.Column(db.String(255), nullable=False)
    Description = db.Column(db.Text, nullable=False)
    StartTime = db.Column(db.DateTime, nullable=False)
    EndTime = db.Column(db.DateTime, nullable=False)

class Vote(db.Model):
    __tablename__ = 'Votes'
    VoteID = db.Column(db.Integer, primary_key=True)
    UserID = db.Column(db.Integer, db.ForeignKey('Users.UserID'))
    VoteType = db.Column(db.String(50), nullable=False)
    TopicID = db.Column(db.Integer, db.ForeignKey('Topics.TopicID'), nullable=False)
    VoteTime = db.Column(db.DateTime, nullable=False)
