import time
import requests
from requests.exceptions import RequestException

class ApiService:
    def __init__(self, base_url, user_id, session=None, max_retries=3, backoff_factor=0.5, min_delay=0.12):
        self.base_url = base_url
        self.user_id = user_id
        self.session = session or requests.Session()
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor
        self.min_delay = min_delay  # para evitar ráfagas

    def _build_url(self):
        return f"{self.base_url}?user_id={self.user_id}"

    def fetch_once(self):
        url = self._build_url()
        for attempt in range(1, self.max_retries + 1):
            try:
                resp = self.session.get(url, timeout=6)
                resp.raise_for_status()
                data = resp.json()
                # aseguramos tipos
                return {"value": int(data["value"]), "category": data["category"]}
            except RequestException as e:
                if attempt == self.max_retries:
                    raise
                delay = self.backoff_factor * (2 ** (attempt - 1))
                time.sleep(delay)
        # si sale por aquí, error
        raise RuntimeError("No se logró obtener datos del API")

    def fetch_with_rate_limit(self):
        """Llama fetch_once y duerme un poquito para evitar ráfagas"""
        result = self.fetch_once()
        time.sleep(self.min_delay)
        return result
