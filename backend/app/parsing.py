import re
from typing import Dict, Any

def extract_metadata(text: str) -> Dict[str, Any]:
    """
    Extracts Date, From, To, and Subject from email text using Regex.
    Expected format is standard email header style.
    """
    metadata = {}
    
    # Regex patterns (basic implementation, can be improved)
    date_pattern = r"(?:Date|Sent):\s*(.*)"
    from_pattern = r"(?:From|Sender):\s*(.*)"
    to_pattern = r"(?:To|Recipient):\s*(.*)"
    subject_pattern = r"(?:Subject|Re):\s*(.*)"
    
    # Search
    date_match = re.search(date_pattern, text, re.IGNORECASE)
    from_match = re.search(from_pattern, text, re.IGNORECASE)
    to_match = re.search(to_pattern, text, re.IGNORECASE)
    subject_match = re.search(subject_pattern, text, re.IGNORECASE)
    
    if date_match:
        metadata["Date"] = date_match.group(1).strip()
    if from_match:
        metadata["From"] = from_match.group(1).strip()
    if to_match:
        metadata["To"] = to_match.group(1).strip()
    if subject_match:
        metadata["Subject"] = subject_match.group(1).strip()
        
    return metadata
