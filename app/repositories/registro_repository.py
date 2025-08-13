from app import db
from app.models import Registro, Barrido

class RegistroRepository:
    def create(self, value, category):
        r = Registro(value=value, category=category)
        db.session.add(r)
        db.session.commit()
        return r

    def list_all(self):
        return Registro.query.all()

    def get(self, registro_id):
        return Registro.query.get(registro_id)

    def get_bad(self):
        return Registro.query.filter_by(category='bad').all()

    def update(self, registro):
        db.session.add(registro)
        db.session.commit()
        return registro

    def delete(self, registro):
        db.session.delete(registro)
        db.session.commit()

class BarridoRepository:
    def log_sweep(self, sweep_number, records_checked, records_improved):
        b = Barrido(sweep_number=sweep_number,
                    records_checked=records_checked,
                    records_improved=records_improved)
        db.session.add(b)
        db.session.commit()
        return b
