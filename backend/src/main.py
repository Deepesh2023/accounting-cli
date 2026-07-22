from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlmodel import SQLModel
from storage.database import engine
from api.inventory import router as inventory_router
from api.parties import router as parties_router
from api.sales import router as sales_router
from api.purchases import router as purchases_router
from api.expenses import router as expenses_router
from api.quotations import router as quotations_router
from api.reports import router as reports_router
from api.company import router as company_router
from api.ledger import router as ledger_router


@asynccontextmanager
async def lifespan(_app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield


app = FastAPI(title="Printos Accounting API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(ValueError)
async def value_error_handler(request, exc):
    return JSONResponse(status_code=400, content={"detail": str(exc)})

@app.exception_handler(Exception)
async def general_error_handler(request, exc):
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})

@app.get("/")
def root():
    return {"status": "ok", "service": "Printos Accounting API"}

app.include_router(inventory_router, prefix="/api/inventory", tags=["Inventory"])
app.include_router(parties_router, prefix="/api/parties", tags=["Parties"])
app.include_router(sales_router, prefix="/api/sales", tags=["Sales"])
app.include_router(purchases_router, prefix="/api/purchases", tags=["Purchases"])
app.include_router(expenses_router, prefix="/api/expenses", tags=["Expenses"])
app.include_router(quotations_router, prefix="/api/quotations", tags=["Quotations"])
app.include_router(reports_router, prefix="/api/reports", tags=["Reports"])
app.include_router(company_router, prefix="/api/company", tags=["Company"])
app.include_router(ledger_router, prefix="/api/ledger", tags=["Ledger"])
