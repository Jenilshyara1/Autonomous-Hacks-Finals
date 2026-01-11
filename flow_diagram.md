# System Flow Diagram

```mermaid
flowchart TD
    %% Styling
    classDef endpoint fill:#f9f,stroke:#333,stroke-width:2px;
    classDef process fill:#e1f5fe,stroke:#333,stroke-width:1px;
    classDef decision fill:#fff9c4,stroke:#333,stroke-width:1px;
    classDef database fill:#e8f5e9,stroke:#333,stroke-width:1px;
    classDef llm fill:#f3e5f5,stroke:#333,stroke-width:2px,stroke-dasharray: 5 5;

    %% Actors and Inputs
    User([User])
    File["File Upload (.eml/.txt)"]
    Text["Text Input (JSON)"]

    %% API Layer
    subgraph API_Layer ["API Layer (FastAPI)"]
        UploadEP["/upload Endpoint"]:::endpoint
        AnalyzeEP["/analyze Endpoint"]:::endpoint
        ExportEP["/export Endpoint"]:::endpoint
    end

    %% Auth Layer
    subgraph Auth ["Authentication"]
        AuthCheck{"Authenticated?"}:::decision
    end

    %% Processing Layer
    subgraph Processing ["Core Processing (processing.py)"]
        Parse["Parse File/Content"]:::process
        Extract["Metadata Extraction (Regex/Headers)"]:::process
        Override["Apply Metadata Overrides"]:::process
        subgraph Classification ["Privilege Analysis"]
            JudgeChain[["Judge Chain (LLM)"]]:::llm
            JudgeCheck{"Is Privileged?"}:::decision
        end
        subgraph Handling ["Privilege Handling"]
            WriterChain[["Writer Chain (LLM)"]]:::llm
            RedactorChain[["Redactor Chain (LLM)"]]:::llm
            FormatDesc["Format Log Description"]:::process
            IdentifyRedaction["Identify Redaction Items"]:::process
        end
    end

    %% Storage Layer
    subgraph Storage ["Database (PostgreSQL/SQLAlchemy)"]
        SaveEmail[("Save to 'emails' Table")]:::database
        SaveLog[("Save to 'privilege_logs' Table")]:::database
        FetchLog[("Fetch User Logs)]:::database
    end

    %% Flow Connections
    User --> File
    User --> Text
    User --> ExportEP
    
    File --> UploadEP
    Text --> AnalyzeEP

    UploadEP --> AuthCheck
    AnalyzeEP --> AuthCheck
    ExportEP --> AuthCheck

    AuthCheck -- Yes --> Parse
    AuthCheck -- Yes --> FetchLog
    AuthCheck -- No --> Error(["401 Unauthorized"])

    Parse --> Extract
    Extract --> Override
    Override --> JudgeChain

    JudgeChain --> JudgeCheck
    
    JudgeCheck -- "Yes (Privileged)" --> WriterChain
    JudgeCheck -- "Yes (Privileged)" --> RedactorChain
    
    JudgeCheck -- "No" --> SaveEmail

    WriterChain --> FormatDesc
    RedactorChain --> IdentifyRedaction

    FormatDesc --> SaveLog
    IdentifyRedaction --> SaveLog
    
    JudgeCheck -- "No" --> SaveLog

    SaveEmail --> SaveLog
    
    FetchLog --> GenCSV["Generate CSV"]:::process
    GenCSV --> Download["Download CSV"]

    %% Dependencies
    SaveEmail -.->|FK: user_id| AuthCheck
```
