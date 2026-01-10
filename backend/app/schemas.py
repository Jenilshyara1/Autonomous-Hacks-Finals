from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

class EmailInput(BaseModel):
    text: str # Raw email text to be parsed
    
    # Optional fields if user wants to provide metadata directly
    date: Optional[str] = None
    sender: Optional[str] = None
    recipient: Optional[str] = None
    subject: Optional[str] = None

class PrivilegeLogOutput(BaseModel):
    is_privileged: bool
    privilege_type: Optional[str] = None
    log_description: Optional[str] = None
    reasoning: Optional[str] = None
    redacted_text: Optional[List[str]] = None # ["Confidential sentence 1...", "Confidential sentence 2..."]

    class Config:
        from_attributes = True

class ProcessingResult(PrivilegeLogOutput):
    metadata: Dict[str, Any]
