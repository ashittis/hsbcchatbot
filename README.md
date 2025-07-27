# Smart Banking Conversational AI

A modular conversational AI designed for banking services, providing secure multi-turn interactions for loan applications, card blocking, mini statements, and banking knowledge queries with mock API backend and session/state management.

## Features

- User authentication via First Name or Customer ID using a comprehensive dataset.
- Intent recognition and slot-filling for tasks like loan application, card blocking, and account statements.
- Retrieval-Augmented Generation (RAG) for answering banking-related knowledge questions.
- Modular design separating dialogue management, NLU, API handlers, and knowledge retrieval.
- Streamlit-based web conversational interface.
- Multi-turn dialogue with context-aware session state and fallback handling.

## Getting Started

### Prerequisites

- Python 3.8+
- See `requirements.txt` for dependencies.

### Installation

```bash
git clone 
cd SmartBankAI
pip install -r requirements.txt
```

### Running the Assistant

```bash
streamlit run app.py
```

Open the displayed local URL in your browser to start interacting with the banking AI.

## Supported Flows & Example Prompts

- **Authentication:** Enter your First Name or Customer ID when prompted.
- **Loan Application:**  
  _Example:_  
  `I want a car loan of 250000`  
  Or respond to bot's prompts for loan type and amount.
- **Block Card:**  
  _Example:_  
  `Block my card`  
  Then provide the last 4 digits when asked.
- **Mini Statement:**  
  _Example:_  
  `Show me last 3 transactions`  
  Then provide your account number.
- **Knowledge Queries:**  
  _Example:_  
  `What is KYC?` or `Explain EMI calculation.`
- **Logout:**  
  Type `logout` to end your session and reset context.

## Project Structure

```
SmartBankAI/
├── app.py              # Streamlit UI entry point
├── dialog_manager.py   # Dialogue flow and API calls
├── nlu.py              # Intent classification rules
├── context_manager.py  # Session state management
├── api_handler.py      # Mock APIs for banking operations
├── rag_engine.py       # Knowledge retrieval & LLM integration
├── data/
│   ├── kb/             # Knowledge base documents
│   └── Comprehensive_Banking_Database.csv
├── requirements.txt
├── README.md
└── docs/               # Attach design documentation here
    └── Architecture_Design.md
```

## Documentation
https://github.com/ashittis/hsbcchatbot/blob/main/hsbc.pdf
