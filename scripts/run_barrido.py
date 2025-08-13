from run import create_app
from app.repositories.registro_repository import RegistroRepository, BarridoRepository
from app.services.api_service import ApiService
from app.services.barrido_service import BarridoService
from config import API_BASE, API_USER_ID

app = create_app()
with app.app_context():
    registro_repo = RegistroRepository()
    barrido_repo = BarridoRepository()
    api = ApiService(API_BASE, API_USER_ID)
    barrido = BarridoService(api, registro_repo, barrido_repo)
    result = barrido.run_full_barrido()
    print("Resultado del barrido:", result)
