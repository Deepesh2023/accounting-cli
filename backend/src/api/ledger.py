from fastapi import APIRouter, Depends, Query, HTTPException, status

from src.ledger.service import LedgerService
from src.api.deps import get_ledger_service


router = APIRouter()


@router.get("/transactions")
def list_transactions(
    account_name: str | None = Query(None),
    service: LedgerService = Depends(get_ledger_service),
):
    if account_name:
        return service.get_entries_for_account(account_name)
    return service.list_all_transactions()


@router.get("/accounts/{account_name}/balance")
def account_balance(
    account_name: str,
    service: LedgerService = Depends(get_ledger_service),
):
    return {"account": account_name, "balance": service.get_balance(account_name)}


@router.get("/gst-summary")
def gst_summary(
    service: LedgerService = Depends(get_ledger_service),
):
    return service.get_gst_summary()


@router.get("/account-balances")
def account_balances(
    accounts: str = Query(..., description="Comma-separated account names"),
    service: LedgerService = Depends(get_ledger_service),
):
    account_list = [a.strip() for a in accounts.split(",") if a.strip()]
    if not account_list:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="At least one account required")
    return service.get_account_balances(account_list)
