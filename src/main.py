from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlmodel import SQLModel
from storage.database import engine
from api.inventory import router as inventory_router
from api.parties import router as parties_router
from api.sales import router as sales_router
from api.purchases import router as purchases_router
from api.expenses import router as expenses_router
from api.quotations import router as quotations_router
from api.reports import router as reports_router


@asynccontextmanager
async def lifespan(_app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield


app = FastAPI(title="Printos Accounting API", lifespan=lifespan)
app.include_router(inventory_router, prefix="/api/inventory", tags=["Inventory"])
app.include_router(parties_router, prefix="/api/parties", tags=["Parties"])
app.include_router(sales_router, prefix="/api/sales", tags=["Sales"])
app.include_router(purchases_router, prefix="/api/purchases", tags=["Purchases"])
app.include_router(expenses_router, prefix="/api/expenses", tags=["Expenses"])
app.include_router(quotations_router, prefix="/api/quotations", tags=["Quotations"])
app.include_router(reports_router, prefix="/api/reports", tags=["Reports"])
