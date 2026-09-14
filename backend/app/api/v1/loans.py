from fastapi import APIRouter, Depends, HTTPException 
from app.models.schemas import LoanCreateRequest 
from app.services.loan_service import LoanService 
from app.core.unit_of_work import UnitOfWork 
from app.api.dependencies import get_uow
# router loans
router = APIRouter(prefix="/loans", tags=["Loans"])
# function create loan
@router.post("/", status_code=201)
def create_loan(req: LoanCreateRequest, uow: UnitOfWork = Depends(get_uow)):
    with uow:
        service = LoanService(uow=uow)
        try:
            loan = service.create_loan(
                client_id=req.client_id,
                copy_ids=req.copy_ids,
                rental_days=req.rental_days
            )
            return loan
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
