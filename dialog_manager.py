import re
import streamlit as st
import pandas as pd
from nlu import classify_intent
from rag_engine import get_rag_answer  

# Load your dataset once at startup
DATASET_PATH = "Comprehensive_Banking_Database.csv"
try:
    df_bank = pd.read_csv(DATASET_PATH)
except Exception as e:
    df_bank = None
    print(f"Failed to load dataset: {e}")

def authenticate_user(user_input):
    if df_bank is None:
        return False, None
    user_input_lower = user_input.strip().lower()

    # Match by First Name (case-insensitive)
    matched_name = df_bank[df_bank['First Name'].str.lower() == user_input_lower]
    matched_id = pd.DataFrame()
    if user_input.isdigit():
        matched_id = df_bank[df_bank['Customer ID'] == int(user_input)]

    if not matched_name.empty:
        user = matched_name.iloc[0]
        return True, user
    elif not matched_id.empty:
        user = matched_id.iloc[0]
        return True, user
    else:
        return False, None

def apply_loan_api(loan_type, amount, user_info):
    name = user_info.get("First Name", "Customer")
    loan_type_cap = loan_type.capitalize()
    return f"Loan application submitted for {name} for a {loan_type_cap} loan of ₹{amount}. Reference ID: LOAN99221."

def block_card_api(card_number, user_info):
    name = user_info.get("First Name", "Customer")
    return f"{name}, your card ending with {card_number} has been successfully blocked."

def get_statement_api(account_number, user_info):
    name = user_info.get("First Name", "Customer")
    return (f"{name}, here are your last 3 transactions for account {account_number}:\n"
            "- ₹500 Debit: Amazon\n- ₹1000 Credit: UPI\n- ₹300 Debit: Zomato")

def handle_user_input(user_input):
    authenticated = st.session_state.get("authenticated", False)
    user_info = st.session_state.get("user_info", None)
    intent = st.session_state.get("intent", None)
    slots = st.session_state.get("slots", {})

    # Step 1: Authentication
    if not authenticated:
        is_auth, user = authenticate_user(user_input)
        if is_auth:
            st.session_state.authenticated = True
            st.session_state.user_info = user.to_dict()
            return (
            f"Welcome {user['First Name']}!\n"
            f"Select an action:\n"
            f"- Apply for loan\n"
            f"- Block a card\n"
            f"- Get account statement\n"
            f"- Ask about KYC\n"
            f"- Logout\n"
            f"How can I help you today?"
        )
        
        else:
            return ("Sorry, I could not find your information. "
                   "Please enter your First Name or Customer ID (account number) to proceed.")
                   

    # Step 2: Intent classification
    if not intent or intent == "unknown":
        intent = classify_intent(user_input.lower())
        st.session_state.intent = intent

    # Step 3: Apply loan intent
    if intent == "apply_loan":
        # Slot: loan_type
        if 'loan_type' not in slots:
            loan_types = ['car', 'home', 'personal', 'education', 'business', 'auto', 'mortgage']
            found_type = None
            user_input_lower = user_input.lower()
            for lt in loan_types:
                if lt in user_input_lower:
                    found_type = 'car' if lt == 'auto' else lt  # normalize 'auto'
                    break
            if found_type:
                slots['loan_type'] = found_type
                st.session_state.slots = slots
            else:
                return ("What type of loan would you like to apply for? "
                        "For example: car, home, or personal.")

        # Slot: loan_amount
        elif 'loan_amount' not in slots:
            amount_match = re.search(r"\b\d+(\.\d+)?\b", user_input.replace(',', ''))
            if amount_match:
                slots['loan_amount'] = amount_match.group(0)
                st.session_state.slots = slots
            else:
                return "Please provide the loan amount you want to apply for."

        # Both slots ready: process loan application
        if 'loan_type' in slots and 'loan_amount' in slots:
            response = apply_loan_api(slots['loan_type'], slots['loan_amount'], user_info)
            # Reset dialog state
            st.session_state.intent = None
            st.session_state.slots = {}
            return response

        # Waiting for more info (no response)
        st.session_state.slots = slots
        return None

    # Step 4: Block card intent
    elif intent == "block_card":
        if 'card_number' not in slots:
            if user_input.isdigit() and len(user_input) >= 4:
                slots['card_number'] = user_input[-4:]
                st.session_state.slots = slots
            else:
                return "Please provide the last 4 digits of your card to block it."
        response = block_card_api(slots['card_number'], user_info)
        st.session_state.intent = None
        st.session_state.slots = {}
        return response

    # Step 5: Account statement intent
    elif intent == "account_statement":
        if 'account_number' not in slots:
            if user_input.isdigit():
                slots['account_number'] = user_input
                st.session_state.slots = slots
            else:
                return "Please provide your account number to retrieve the statement."
        response = get_statement_api(slots['account_number'], user_info)
        st.session_state.intent = None
        st.session_state.slots = {}
        return response

    # Step 6: Knowledge query intent (RAG)
    elif intent == "knowledge_query":
        return get_rag_answer(user_input)

    # Step 7: Logout command
    elif user_input.lower() in ["logout", "exit"]:
        st.session_state.authenticated = False
        st.session_state.user_info = None
        st.session_state.intent = None
        st.session_state.slots = {}
        return "You have been logged out. Please enter your First Name or Customer ID to start again."

    # Step 8: Fallback
    else:
        return "Sorry, I didn’t understand that. Try asking about loans, statements, or KYC."
    if not intent or intent == "unknown":
        intent = classify_intent(user_input)
        st.session_state.intent = intent

    # Handle known intents like apply_loan, block_card, account_statement, etc.
    if intent == "apply_loan":
        # ... your existing code ...
        pass

    elif intent == "block_card":
        # ... your existing code ...
        pass

    elif intent == "account_statement":
        # ... your existing code ...
        pass

    elif intent == "knowledge_query":
        # Call RAG for domain related questions
        return get_rag_answer(user_input)

    # NEW: for unknown or other queries, call RAG as fallback
    elif intent == "unknown":
        answer = get_rag_answer(user_input)
        if answer.strip():
            return answer
        else:
            return "Sorry, I do not have information on that topic."

    # add logout and fallback as usual
    elif user_input.lower() in ["logout", "exit"]:
        # Reset session
        st.session_state.authenticated = False
        st.session_state.user_info = None
        st.session_state.intent = None
        st.session_state.slots = {}
        return "You have been logged out. Please enter your customer ID to start again."

    else:
        return "Sorry, I didn’t understand that. Please ask about loans, cards, statements, or general banking questions."
def get_account_info(user_info):
    name = user_info.get("First Name", "Customer")
    account_type = user_info.get("Account Type", "N/A")
    account_balance = user_info.get("Account Balance", "N/A")
    date_opened = user_info.get("Date Of Account Opening", "N/A")
    last_txn_date = user_info.get("Last Transaction Date", "N/A")
    
    info = (f"{name}, here is your account information:\n"
            f"- Account Type: {account_type}\n"
            f"- Account Balance: ₹{account_balance}\n"
            f"- Date Opened: {date_opened}\n"
            f"- Last Transaction Date: {last_txn_date}")
    return info

