from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Email, PrivilegeLog
from ..schemas import EmailInput, ProcessingResult, PrivilegeLogOutput
from ..parsing import extract_metadata
from ..chains import get_judge_chain, get_writer_chain, get_redactor_chain, PrivilegeClassification

router = APIRouter()

@router.post("/analyze", response_model=ProcessingResult)
async def analyze_email(email_input: EmailInput, db: Session = Depends(get_db)):
    # 1. Store Email (optional, but good for record)
    # For simplicity, we just process it first
    
    # 2. Metadata Extraction (Deterministic)
    metadata = extract_metadata(email_input.text)
    # Override with user provided if any
    if email_input.date: metadata["Date"] = email_input.date
    if email_input.sender: metadata["From"] = email_input.sender
    if email_input.recipient: metadata["To"] = email_input.recipient
    if email_input.subject: metadata["Subject"] = email_input.subject
    
    sender = metadata.get("From", "Unknown")
    recipient = metadata.get("To", "Unknown")
    subject = metadata.get("Subject", "No Subject")
    body = email_input.text # In real parsing, we might separate body from headers
    
    # 3. Step 2: Privilege Classification
    judge_chain = get_judge_chain()
    try:
        judge_result = judge_chain.invoke({
            "sender": sender,
            "recipient": recipient,
            "subject": subject,
            "body": body
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM Classification Error: {str(e)}")

    # Is result a dict or object? JsonOutputParser returns dict usually
    is_privileged = judge_result.get("is_privileged", False)
    privilege_type = judge_result.get("privilege_type")
    reasoning = judge_result.get("reasoning")

    description = None
    redaction_indices = None

    # 4. Step 3 & 4: If Privileged
    if is_privileged:
        # Writer
        writer_chain = get_writer_chain()
        writer_result = writer_chain.invoke({
            "reasoning": reasoning,
            "body": body
        })
        description = writer_result.get("log_description")

        # Redactor
        redactor_chain = get_redactor_chain()
        redactor_result = redactor_chain.invoke({
            "body": body
        })
        redaction_items = redactor_result.get("items", [])

    # 5. Save to DB
    db_email = Email(
        sender=sender,
        recipient=recipient,
        subject=subject,
        body=body,
        # date=... parse date string to datetime if needed
    )
    db.add(db_email)
    db.commit()
    db.refresh(db_email)

    db_log = PrivilegeLog(
        email_id=db_email.id,
        is_privileged=is_privileged,
        privilege_type=privilege_type,
        log_description=description,
        reasoning=reasoning,
        redacted_text=str(redaction_items) if redaction_items else None
    )
    db.add(db_log)
    db.commit()

    return ProcessingResult(
        metadata=metadata,
        is_privileged=is_privileged,
        privilege_type=privilege_type,
        log_description=description,
        reasoning=reasoning,
        redacted_text=redaction_items
    )
