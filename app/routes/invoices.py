from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.models import Invoice
from app.schemas import InvoiceRequest
from app.services.llm_service import extract_invoice_data
from app.utils.parser import safe_parse_llm_output
import json

router = APIRouter()

# DB dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/invoices")
def create_invoice(request: InvoiceRequest, db: Session = Depends(get_db)):
    llm_response = extract_invoice_data(request.raw_text)
    data = safe_parse_llm_output(llm_response)

    invoice = Invoice(
        vendor=data["vendor"],
        amount=data["amount"],
        due_date=data["due_date"],
        raw_text=request.raw_text,
        line_items=json.dumps(data["line_items"]),
    )

    db.add(invoice)
    db.commit()
    db.refresh(invoice)

    return {
        "invoice_id": invoice.id,
        **data
    }


@router.get("/invoices")
def get_invoices(db: Session = Depends(get_db)):
    invoices = db.query(Invoice).all()

    result = []
    for inv in invoices:
        result.append({
            "id": inv.id,
            "vendor": inv.vendor,
            "amount": inv.amount,
            "due_date": inv.due_date,
            "line_items": json.loads(inv.line_items)
        })

    return result