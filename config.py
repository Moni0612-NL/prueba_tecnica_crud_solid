from dotenv import load_dotenv
import os

# Carga las variables de entorno desde el archivo .env
load_dotenv()

# Base de datos
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///prueba.db")

# API externa
API_USER_ID = os.getenv("API_USER_ID", "M9JRA3")
API_BASE = os.getenv("API_BASE", "https://4advance.co/testapi/get.php")
