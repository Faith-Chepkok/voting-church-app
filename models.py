from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    votes = db.Column(db.String(0), unique=True, nullable=False)
    
class Voter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String(200), nullable=False)
    has_voted = db.Column(db.Boolean, default=False, nullable=False)

class Vote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    voter_id= db.Column(db.Integer, db.ForeignKey('voter.id'), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=False)

