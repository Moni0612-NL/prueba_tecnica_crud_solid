import json
import types
from app.services.api_service import ApiService

class DummyResponse:
    def __init__(self, json_data, status_code=200):
        self._json = json_data
        self.status_code = status_code
    def raise_for_status(self):
        if self.status_code >= 400:
            raise Exception("status")
    def json(self):
        return self._json

def test_fetch_once_monkeypatch(monkeypatch):
    called = {}
    def fake_get(url, timeout):
        called['url'] = url
        return DummyResponse({"value": "80", "category": "good"})
    session = type("S", (), {"get": staticmethod(fake_get)})()
    api = ApiService("https://example.com", "ID", session=session)
    res = api.fetch_once()
    assert res['value'] == 80
    assert res['category'] == "good"
