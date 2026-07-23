from src.company.models import Company
from src.company.repository import CompanyRepository

class CompanyService:
    def __init__(self, repository: CompanyRepository):
        self.repository = repository

    def get_profile(self) -> Company | None:
        return self.repository.get_company()

    def update_profile(self, company_data: Company) -> Company:
        return self.repository.update_company(company_data)
