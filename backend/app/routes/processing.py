from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from ..database import get_db
from ..routes.auth import get_current_user
from ..models import Email, PrivilegeLog, User
from ..schemas import EmailInput, ProcessingResult
from ..parsing import extract_metadata
from ..chains import get_judge_chain, get_writer_chain, get_redactor_chain
import email
import io
import csv

router = APIRouter()

async def process_and_save_email(text: str, metadata_override: dict, db: AsyncSession, user_id: int | None = None) -> ProcessingResult:
    """
    Shared logic to process email text, run chains, and save to DB.
    metadata_override can contain keys: Date, From, To, Subject
    """
    # 1. Metadata Extraction (Deterministic) from text
    metadata = extract_metadata(text)
    
    # ... (unchanged metadata merge logic) ...
    for k, v in metadata_override.items():
        if v:
            metadata[k] = v
            
    sender = metadata.get("From", "Unknown")
    recipient = metadata.get("To", "Unknown")
    subject = metadata.get("Subject", "No Subject")
    date_val = metadata.get("Date") 
    
    # 3. Privilege Classification
    judge_chain = get_judge_chain()
    try:
        # ASYNC LANGCHAIN CALL
        judge_result = await judge_chain.ainvoke({
            "sender": sender,
            "recipient": recipient,
            "subject": subject,
            "body": text
        })
    except Exception as e:
        print(f"Error in judge chain: {e}")
        raise HTTPException(status_code=500, detail=f"LLM Classification Error: {str(e)}")

    is_privileged = judge_result.get("is_privileged", False)
    privilege_type = judge_result.get("privilege_type")
    reasoning = judge_result.get("reasoning")

    description = None
    redaction_items = None

    # 4. If Privileged, run other chains
    if is_privileged:
        # Writer
        writer_chain = get_writer_chain()
        # ASYNC LANGCHAIN CALL
        writer_result = await writer_chain.ainvoke({
            "reasoning": reasoning,
            "body": text
        })
        description = writer_result.get("log_description")

        # Redactor
        redactor_chain = get_redactor_chain()
        # ASYNC LANGCHAIN CALL
        redactor_result = await redactor_chain.ainvoke({
            "body": text
        })
        redaction_items = redactor_result.get("items", [])

    # 5. Save to DB (Async)
    db_email = Email(
        sender=sender,
        recipient=recipient,
        subject=subject,
        body=text,
        user_id=user_id
    )
    db.add(db_email)
    await db.commit()
    await db.refresh(db_email)

    db_log = PrivilegeLog(
        email_id=db_email.id,
        is_privileged=is_privileged,
        privilege_type=privilege_type,
        log_description=description,
        reasoning=reasoning,
        redacted_text=str(redaction_items) if redaction_items else None
    )
    db.add(db_log)
    await db.commit()

    return ProcessingResult(
        metadata=metadata,
        is_privileged=is_privileged,
        privilege_type=privilege_type,
        log_description=description,
        reasoning=reasoning,
        redacted_text=redaction_items
    )

@router.post("/analyze", response_model=ProcessingResult)
async def analyze_email(
    email_input: EmailInput, 
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Existing JSON endpoint.
    """
    overrides = {}
    if email_input.date: overrides["Date"] = email_input.date
    if email_input.sender: overrides["From"] = email_input.sender
    if email_input.recipient: overrides["To"] = email_input.recipient
    if email_input.subject: overrides["Subject"] = email_input.subject
    
    return await process_and_save_email(email_input.text, overrides, db, user_id=current_user.id)

@router.post("/upload", response_model=ProcessingResult)
async def upload_email(
    file: UploadFile = File(...), 
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Upload .eml or .txt file to be processed.
    """
    content = await file.read()
    filename = file.filename.lower()
    
    text_body = ""
    metadata = {}
    
    if filename.endswith(".eml"):
        msg = email.message_from_bytes(content)
        
        metadata["Subject"] = msg.get("Subject", "No Subject")
        metadata["From"] = msg.get("From", "Unknown")
        metadata["To"] = msg.get("To", "Unknown")
        metadata["Date"] = msg.get("Date")
        
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    payload = part.get_payload(decode=True)
                    if payload:
                        text_body = payload.decode(errors="replace")
                        break
            if not text_body:
                 for part in msg.walk():
                    if part.get_content_maintype() == 'text':
                         payload = part.get_payload(decode=True)
                         if payload:
                            text_body = payload.decode(errors="replace")
                            break
        else:
             payload = msg.get_payload(decode=True)
             if payload:
                text_body = payload.decode(errors="replace")
                
    else:
        # Assume text file
        text_body = content.decode(errors="replace")
        metadata["Subject"] = filename
    
    return await process_and_save_email(text_body, metadata, db, user_id=current_user.id)

@router.get("/export")
async def export_privilege_log(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Generate CSV of the privilege log.
    Async DB query.
    """
    # Async Query filtered by user
    query = (
        select(Email, PrivilegeLog)
        .join(PrivilegeLog, Email.id == PrivilegeLog.email_id)
        .where(Email.user_id == current_user.id)
    )
    result = await db.execute(query)
    results = result.all()
    
    output = io.StringIO()
    writer = csv.writer(output)
    
    writer.writerow(["DocID", "Date", "Author", "Recipient", "Privilege Type", "Description"])
    
    for email_row, log_row in results:
        doc_id = f"CTRL{email_row.id:06d}"
        date_str = email_row.date.strftime("%Y-%m-%d") if email_row.date else ""
        
        writer.writerow([
            doc_id,
            date_str,
            email_row.sender,
            email_row.recipient,
            log_row.privilege_type if log_row.is_privileged else "Not Privileged",
            log_row.log_description if log_row.log_description else ""
        ])
    
    output.seek(0)
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=privilege_log.csv"}
    )
