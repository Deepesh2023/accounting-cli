from uuid import UUID
from sqlmodel import Session, select
from parties.models import Party, PartyType
from decimal import Decimal

class PartyRepository:
    def __init__(self, session: Session):
        self.session = session

    def add_party(self, party: Party) -> Party:
        self.session.add(party)
        self.session.commit()
        self.session.refresh(party)
        return party

    def get_party(self, party_id: UUID) -> Party | None:
        return self.session.get(Party, party_id)

    def list_parties(self, party_type: PartyType | None = None) -> list[Party]:
        stmt = select(Party)
        if party_type:
            stmt = stmt.where(Party.party_type == party_type)
        return self.session.execute(stmt).scalars().all()

    def update_balance(self, party_id: UUID, amount: Decimal) -> Party | None:
        """
        Updates the running balance and handles the "Flip" logic.
        If a Debtor's balance becomes negative, they become a Creditor and vice versa.
        """
        party = self.get_party(party_id)
        if not party:
            return None

        party.balance += amount
        
        # Flip logic: If balance sign changes, flip the PartyType
        if party.balance > 0 and party.party_type == PartyType.CREDITOR:
            party.party_type = PartyType.DEBTOR
        elif party.balance < 0 and party.party_type == PartyType.DEBTOR:
            party.party_type = PartyType.CREDITOR
            # Store balance as absolute for the new type if needed, 
            # but usually, we keep the sign for internal math.
            # The report implies the type reflects the current state.

        self.session.commit()
        self.session.refresh(party)
        return party

    def update_party(self, party_data: Party) -> Party:
        db_party = self.get_party(party_data.party_id)
        if not db_party:
            raise ValueError("Party not found")
        
        # Update fields
        db_party.name = party_data.name
        db_party.address = party_data.address
        db_party.phone = party_data.phone
        
        self.session.commit()
        self.session.refresh(db_party)
        return db_party

    def delete_party(self, party_id: UUID) -> bool:
        party = self.get_party(party_id)
        if not party:
            return False
        self.session.delete(party)
        self.session.commit()
        return True
