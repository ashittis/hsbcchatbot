def classify_intent(text):
    text = text.lower()
    if "loan" in text:
        return "apply_loan"
    elif "block" in text and "card" in text:
        return "block_card"
    elif "statement" in text or "transactions" in text:
        return "account_statement"
    elif "balance" in text or "account info" in text or "account information" in text or "account details" in text:
        return "account_info"
    elif "kyc" in text or "emi" in text or "interest" in text or "guidelines" in text:
        return "knowledge_query"
    else:
        return "unknown"
