from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin
from datetime import datetime

# Setting up the metadata for SQLAlchemy to follow a custom naming convention
metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

# Initialize SQLAlchemy with the custom metadata
db = SQLAlchemy(metadata=metadata)

# Define the Message model
class Message(db.Model, SerializerMixin):
    __tablename__ = 'messages'

    # Define the columns for the Message table
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(280), nullable=False)
    username = db.Column(db.String(80), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # SerializerMixin automatically provides a .to_dict() method
