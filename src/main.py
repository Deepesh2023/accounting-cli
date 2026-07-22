from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlmodel import SQLModel
from storage.database import engine
from api.inventory import router as inventory_router
from api.parties import router as parties_router
from api.sales import router as sales_router


@asynccontextmanager
async def lifespan(_app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield


app = FastAPI(title="Printos Accounting API", lifespan=lifespan)
app.include_router(inventory_router, prefix="/api/inventory", tags=["Inventory"])
app.include_router(parties_router, prefix="/api/parties", tags=["Parties"])
app.include_router(sales_router, prefix="/api/sales", tags=["Sales"])
