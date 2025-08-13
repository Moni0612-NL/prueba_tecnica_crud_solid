import pytest
from unittest.mock import MagicMock
from app.services.barrido_service import BarridoService



class Registro:
    def __init__(self, value, category, attempts=0):
        self.value = value
        self.category = category
        self.attempts = attempts


@pytest.fixture
def mock_deps():
    api_service = MagicMock()
    registro_repo = MagicMock()
    barrido_repo = MagicMock()
    return api_service, registro_repo, barrido_repo


def test_run_full_barrido_improves_records(mock_deps):
    api_service, registro_repo, barrido_repo = mock_deps

    # Mock data
    registro1 = Registro(value="old1", category="bad")
    registro2 = Registro(value="old2", category="bad")

    registro_repo.get_bad.side_effect = [
        [registro1, registro2],  # Primera pasada
        []  # Segunda pasada (sin malos)
    ]

    api_service.fetch_with_rate_limit.side_effect = [
        {"value": "new1", "category": "good"},   # mejora
        {"value": "same2", "category": "bad"}    # no mejora
    ]

    service = BarridoService(api_service, registro_repo, barrido_repo, per_call_delay=0)

    result = service.run_full_barrido()

    assert result["sweeps"] == 1
    assert registro1.value == "new1"
    assert registro1.category == "good"
    assert registro1.attempts == 1
    assert registro2.category == "bad"
    assert registro2.attempts == 1

    registro_repo.update.assert_any_call(registro1)
    registro_repo.update.assert_any_call(registro2)
    barrido_repo.log_sweep.assert_called_once_with(
        sweep_number=1, records_checked=2, records_improved=1
    )


def test_run_full_barrido_handles_exceptions(mock_deps):
    api_service, registro_repo, barrido_repo = mock_deps

    registro1 = Registro(value="old", category="bad")

    registro_repo.get_bad.side_effect = [
        [registro1],
        []
    ]

    api_service.fetch_with_rate_limit.side_effect = Exception("API error")

    service = BarridoService(api_service, registro_repo, barrido_repo, per_call_delay=0)

    result = service.run_full_barrido()

    assert result["sweeps"] == 1
    assert registro1.attempts == 1  # incluso con error aumenta
    registro_repo.update.assert_called_with(registro1)
    barrido_repo.log_sweep.assert_called_once_with(
        sweep_number=1, records_checked=1, records_improved=0
    )
