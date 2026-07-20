from uuid import UUID
from quotation.models import Quotation, QuotationItem
from quotation.repository import QuotationRepository

class QuotationService:
    def __init__(self, repository: QuotationRepository):
        self.repository = repository

    def create_quotation(self, quotation: Quotation) -> Quotation:
        return self.repository.add_quotation(quotation)

    def get_all_quotations(self) -> list[Quotation]:
        return self.repository.list_quotations()

    def get_quotation_by_id(self, q_id: UUID | str) -> Quotation | None:
        uid = UUID(q_id) if isinstance(q_id, str) else q_id
        return self.repository.get_quotation(uid)

    def remove_quotation(self, q_id: UUID | str) -> bool:
        uid = UUID(q_id) if isinstance(q_id, str) else q_id
        return self.repository.delete_quotation(uid)
