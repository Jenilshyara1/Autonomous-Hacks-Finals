from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
from typing import List, Optional
from .llm import llm

# --- Data Models for LLM Output ---

class PrivilegeClassification(BaseModel):
    is_privileged: bool = Field(description="Whether the email is Attorney-Client Privileged or Work Product")
    privilege_type: Optional[str] = Field(description="Type of privilege: 'Attorney-Client', 'Work Product', or None")
    reasoning: str = Field(description="Brief legal reasoning for the classification")

class PrivilegeDescription(BaseModel):
    log_description: str = Field(description="A neutral, professional log identification description that does not reveal sensitive info")

class RedactionOutput(BaseModel):
    items: List[str] = Field(description="List of exact text strings from the email that contain privileged information")

# --- Prompts ---

judge_system_prompt = """You are a senior litigation attorney. Your task is to analyze email content and determine if it is privileged.

RULES:
1. Identify if the document is Attorney-Client Privileged (ACP) or Attorney Work Product (AWP).
2. ACP requires communication between client and counsel for the purpose of legal advice.
3. AWP requires document prepared in anticipation of litigation.
4. If NOT privileged, return is_privileged=False.
5. Provide clear reasoning.
"""

writer_system_prompt = """You are a senior litigation attorney. Your task is to generate a Privilege Log entry for a privileged email.

RULES:
1. The description must be neutral and professional.
2. DO NOT reveal the confidential advice given or specific sensitive details (dollar amounts, strategy).
3. Use the format: "[Type of communication] regarding [General Topic]."
4. Example: "Confidential communication between Client and Counsel requesting legal advice regarding contractual liability."
"""

redactor_system_prompt = """You are a senior litigation attorney. Your task is to identify specific sentences in an email that contain legal advice or privileged information for redaction.
Return the EXACT text strings of the sensitive sentences or clauses from the provided email body.
If there is no sensitive text, return an empty list.
"""

# --- Chains ---

def get_judge_chain():
    parser = JsonOutputParser(pydantic_object=PrivilegeClassification)
    prompt = ChatPromptTemplate.from_messages([
        ("system", judge_system_prompt),
        ("user", "Sender: {sender}\nRecipient: {recipient}\nSubject: {subject}\n\nEmail Body:\n{body}\n\n{format_instructions}")
    ]).partial(format_instructions=parser.get_format_instructions())
    return prompt | llm | parser

def get_writer_chain():
    parser = JsonOutputParser(pydantic_object=PrivilegeDescription)
    prompt = ChatPromptTemplate.from_messages([
        ("system", writer_system_prompt),
        ("user", "Privilege Reason: {reasoning}\n\nEmail Body:\n{body}\n\n{format_instructions}")
    ]).partial(format_instructions=parser.get_format_instructions())
    return prompt | llm | parser

def get_redactor_chain():
    parser = JsonOutputParser(pydantic_object=RedactionOutput)
    prompt = ChatPromptTemplate.from_messages([
        ("system", redactor_system_prompt),
        ("user", "Email Body:\n{body}\n\n{format_instructions}")
    ]).partial(format_instructions=parser.get_format_instructions())
    return prompt | llm | parser
