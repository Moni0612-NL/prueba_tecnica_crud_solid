from datetime import datetime
from . import db

class Registro(db.Model):
    __tablename__ = 'registros'
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(10), nullable=False)
    attempts = db.Column(db.Integer, default=1, nullable=False)  # cuenta cuántas llamadas se hicieron
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "value": self.value,
            "category": self.category,
            "attempts": self.attempts,
            "created_at": self.created_at.isoformat()
        }

class Barrido(db.Model):
    __tablename__ = 'barridos'
    id = db.Column(db.Integer, primary_key=True)
    sweep_number = db.Column(db.Integer, nullable=False)
    records_checked = db.Column(db.Integer)
    records_improved = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
