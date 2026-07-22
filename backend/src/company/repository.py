from sqlmodel import Session, select
from company.models import Company

class CompanyRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_company(self) -> Company | None:
        # Assuming only one company profile exists
        return self.session.exec(select(Company)).first()

    def update_company(self, company: Company) -> Company:
        db_company = self.get_company()
        if not db_company:
            self.session.add(company)
            self.session.commit()
            self.session.refresh(company)
            return company
        
        db_company.name = company.name
        db_company.business_type = company.business_type
        db_company.category = company.category
        db_company.beginning_date = company.beginning_date
        db_company.phone = company.phone
        db_company.email = company.email
        db_company.address = company.address
        db_company.logo_path = company.logo_path
        db_company.qr_path = company.qr_path
        
        self.session.commit()
        self.session.refresh(db_company)
        return db_company
