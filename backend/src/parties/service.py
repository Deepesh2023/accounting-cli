import uuid
from uuid import UUID
from decimal import Decimal
from src.parties.models import Party, PartyType
from src.parties.repository import PartyRepository

class PartyService:
    def __init__(self, repository: PartyRepository):
        self.repository = repository

    def create_party(self, name: str, party_type: PartyType, balance: Decimal = Decimal("0"), address: str = None, phone: str = None) -> Party:
        if not name:
            raise ValueError("Party name cannot be empty")
        
        party = Party(
            party_id=uuid.uuid4(),
            name=name,
            party_type=party_type,
            balance=balance,
            address=address,
            phone=phone
        )
        return self.repository.add_party(party)

    def get_party(self, party_id: UUID) -> Party:
        party = self.repository.get_party(party_id)
        if not party:
            raise ValueError(f"Party with id {party_id} not found")
        return party

    def list_parties(self, party_type: PartyType | None = None) -> list[Party]:
        return self.repository.list_parties(party_type)

    def update_party_info(self, party_id: UUID, name: str = None, address: str = None, phone: str = None) -> Party:
        party = self.get_party(party_id)

        updated_data = Party(
            party_id=party.party_id,
            name=name if name else party.name,
            party_type=party.party_type,
            balance=party.balance,
            address=address if address else party.address,
            phone=phone if phone else party.phone,
            state=party.state,
            gstin=party.gstin,
        )
        return self.repository.update_party(updated_data)

    def delete_party(self, party_id: UUID) -> None:
        result = self.repository.delete_party(party_id)
        if not result:
            raise ValueError(f"Party with id {party_id} not found")

    def adjust_balance(self, party_id: UUID, amount: Decimal) -> Party:
        """
        Adjusts party balance. 
        Positive amount increases balance, negative decreases it.
        """
        result = self.repository.update_balance(party_id, amount)
        if not result:
            raise ValueError(f"Party with id {party_id} not found")
        return result
