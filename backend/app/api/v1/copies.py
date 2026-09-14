from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
# pyrefly: ignore [missing-import]
from opensearchpy import OpenSearch
from app.repositories.copy_repository import CopyRepository
from app.api.dependencies import get_opensearch_db
# router copies
router = APIRouter(prefix="/copies", tags=["Copies"])
# class request retire copy
class RetireCopyRequest(BaseModel):
    reason: str  # "stolen", "lost", "damaged"
    notes: Optional[str] = None
# funcion retire copy
@router.post("/{copy_id}/retire")
def retire_copy(copy_id: str, req: RetireCopyRequest, db: OpenSearch = Depends(get_opensearch_db)):
    repo = CopyRepository(client=db)
    success = repo.retire_copy_painless(copy_id, reason=req.reason, notes=req.notes)
    if not success:
        raise HTTPException(status_code=400, detail=f"No se pudo registrar la baja de la copia '{copy_id}'.")
    return {"message": f"Copia '{copy_id}' retirada exitosamente", "reason": req.reason}
