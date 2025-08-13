import time
from run import create_app
from app import db
from app.services.api_service import ApiService
from app.repositories.registro_repository import RegistroRepository

from config import API_BASE, API_USER_ID

app = create_app()
with app.app_context():
    registro_repo = RegistroRepository()
    api = ApiService(API_BASE, API_USER_ID)
    print("Iniciando carga inicial de 100 llamadas...")
    for i in range(100):
        try:
            data = api.fetch_with_rate_limit()
        except Exception as e:
            print(f"Error en llamada {i+1}: {e}")
            continue
        r = registro_repo.create(value=data['value'], category=data['category'])
        print(f"{i+1}/100 -> id={r.id} cat={r.category} value={r.value}")
    print("Carga inicial finalizada.")
