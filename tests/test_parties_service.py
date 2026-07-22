import pytest
from uuid import uuid4, UUID
from decimal import Decimal
from unittest.mock import Mock, patch
from dataclasses import dataclass

from parties.models import Party, PartyType
from parties.service import PartyService

@dataclass
class PartyMock:
    party_id: UUID
    name: str
    party_type: PartyType
    balance: Decimal
    address: str = None
    phone: str = None
    state: str = ""
    gstin: str = None

@pytest.fixture
def mock_repo():
    return Mock()

@pytest.fixture
def service(mock_repo):
    return PartyService(mock_repo)

def test_create_party_success(service, mock_repo):
    mock_repo.add_party.side_effect = lambda p: p
    
    party = service.create_party("John Doe", PartyType.DEBTOR, Decimal("100"), "Addr", "123")
    
    assert party.name == "John Doe"
    assert party.party_type == PartyType.DEBTOR
    assert party.balance == Decimal("100")
    mock_repo.add_party.assert_called_once()

def test_create_party_empty_name(service):
    with pytest.raises(ValueError, match="Party name cannot be empty"):
        service.create_party("", PartyType.DEBTOR)

def test_get_party_success(service, mock_repo):
    p_id = uuid4()
    party = PartyMock(p_id, "John", PartyType.DEBTOR, Decimal("0"))
    mock_repo.get_party.return_value = party
    
    assert service.get_party(p_id) == party

def test_get_party_not_found(service, mock_repo):
    mock_repo.get_party.return_value = None
    with pytest.raises(ValueError, match="not found"):
        service.get_party(uuid4())

def test_list_parties(service, mock_repo):
    p1 = PartyMock(uuid4(), "P1", PartyType.DEBTOR, Decimal("0"))
    p2 = PartyMock(uuid4(), "P2", PartyType.CREDITOR, Decimal("0"))
    mock_repo.list_parties.return_value = [p1, p2]
    
    assert service.list_parties() == [p1, p2]
    mock_repo.list_parties.assert_called_once_with(None)

def test_update_party_info(service, mock_repo):
    p_id = uuid4()
    party = PartyMock(p_id, "Old Name", PartyType.DEBTOR, Decimal("0"), state="Karnataka", gstin="29ABCDE1234F1Z5")
    mock_repo.get_party.return_value = party
    mock_repo.update_party.side_effect = lambda p: p

    updated = service.update_party_info(p_id, name="New Name")

    assert updated.name == "New Name"
    assert updated.state == "Karnataka"
    assert updated.gstin == "29ABCDE1234F1Z5"
    mock_repo.update_party.assert_called_once()

def test_adjust_balance_success(service, mock_repo):
    p_id = uuid4()
    party = PartyMock(p_id, "John", PartyType.DEBTOR, Decimal("100"))
    mock_repo.update_balance.return_value = party
    
    result = service.adjust_balance(p_id, Decimal("50"))
    
    assert result == party
    mock_repo.update_balance.assert_called_once_with(p_id, Decimal("50"))

def test_adjust_balance_not_found(service, mock_repo):
    mock_repo.update_balance.return_value = None
    with pytest.raises(ValueError, match="not found"):
        service.adjust_balance(uuid4(), Decimal("50"))

def test_delete_party_success(service, mock_repo):
    p_id = uuid4()
    mock_repo.delete_party.return_value = True

    service.delete_party(p_id)

    mock_repo.delete_party.assert_called_once_with(p_id)

def test_delete_party_not_found(service, mock_repo):
    mock_repo.delete_party.return_value = False

    with pytest.raises(ValueError, match="not found"):
        service.delete_party(uuid4())
