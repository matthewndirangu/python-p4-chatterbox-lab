from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from models import db, Message  # Import the Message model and db
from sqlalchemy.orm import Session

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

# Route to get all messages
@app.route('/messages', methods=['GET'])
def messages():
    messages = Message.query.order_by(Message.created_at.asc()).all()
    return jsonify([message.to_dict() for message in messages])

# Route to create a new message
@app.route('/messages', methods=['POST'])
def create_message():
    data = request.get_json()
    new_message = Message(body=data['body'], username=data['username'])
    db.session.add(new_message)
    db.session.commit()
    return jsonify(new_message.to_dict()), 201

# Route to get, update, or delete a specific message by ID
@app.route('/messages/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
def messages_by_id(id):
    # Use the session from the db instance
    session = db.session
    message = session.get(Message, id)
    
    if not message:
        return make_response(jsonify({"error": "Message not found"}), 404)

    if request.method == 'GET':
        return jsonify(message.to_dict())

    if request.method == 'PATCH':
        data = request.get_json()
        message.body = data.get('body', message.body)
        session.commit()
        return jsonify(message.to_dict())

    if request.method == 'DELETE':
        session.delete(message)
        session.commit()
        return make_response(jsonify({"message": "Message deleted"}), 200)

if __name__ == '__main__':
    app.run(port=5555)
