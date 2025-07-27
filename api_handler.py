def apply_loan_api(loan_type, amount, user_info):
    name = user_info.get("First Name", "Customer")
    return f"Loan application submitted for {name} for a {loan_type} loan of ₹{amount}. Reference ID: LOAN99221."

def block_card_api(card_number, user_info):
    name = user_info.get("First Name", "Customer")
    # Optionally add validation that card belongs to the user if your dataset/card info is accessible here
    return f"{name}, your card ending with {card_number} has been successfully blocked."

def get_statement_api(account_number, user_info):
    name = user_info.get("First Name", "Customer")
    # Optionally, query dataset transactions for this account number dynamically
    return (f"{name}, here are your last 3 transactions for account {account_number}:\n"
            "- ₹500 Debit: Amazon\n- ₹1000 Credit: UPI\n- ₹300 Debit: Zomato")
