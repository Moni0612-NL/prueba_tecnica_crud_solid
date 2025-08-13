from run import create_app
from app import db
from app.models import Registro, Barrido

app = create_app()
with app.app_context():
    total = db.session.query(Registro).count()
    dist = db.session.execute(db.text("""
        SELECT category, COUNT(*) as cantidad
        FROM registros
        GROUP BY category
        ORDER BY category
    """)).all()
    llamadas = db.session.execute(db.text("""
        SELECT COALESCE(SUM(attempts),0) as llamadas_totales FROM registros
    """)).scalar()
    barridos = db.session.query(Barrido).count()

    print("=== ESTADO ===")
    print(f"Total registros: {total}")
    print("Distribución por categoría:")
    for c, n in dist:
        print(f"  - {c}: {n}")
    print(f"Llamadas totales (SUM attempts): {llamadas}")
    print(f"Barridos realizados: {barridos}")
