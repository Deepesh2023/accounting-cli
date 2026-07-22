from fastapi import APIRouter, Depends

from reports.service import ReportService
from api.deps import get_report_service


router = APIRouter()


@router.get("/trading-account")
def trading_account(
    service: ReportService = Depends(get_report_service),
):
    return service.get_trading_account()


@router.get("/profit-and-loss")
def profit_and_loss(
    service: ReportService = Depends(get_report_service),
):
    trading = service.get_trading_account()
    return service.get_profit_and_loss(trading["gross_profit"])


@router.get("/balance-sheet")
def balance_sheet(
    service: ReportService = Depends(get_report_service),
):
    return service.get_balance_sheet()


@router.get("/outstanding")
def outstanding_report(
    service: ReportService = Depends(get_report_service),
):
    return service.get_outstanding_report()


@router.get("/transactions")
def transaction_history(
    service: ReportService = Depends(get_report_service),
):
    return service.get_transaction_history()
