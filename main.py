import uuid
from datetime import datetime
from database import get_connection
connection = get_connection()
cursor = connection.cursor()

def add_new_transaction():
    acct_name = input("Acct_name: ")
    cursor.execute("SELECT id, acct_balance FROM accounts WHERE acct_name = ?", (acct_name,))
    result = cursor.fetchone()
    if result == None:
        print("This account does not exist")
        return
    acct_id,balance = result
    try: 
        amount = int(input("Amount: "))
        if amount <= 0:
            print("Invalid amount.")
            return
    except ValueError:
        print("Invalid amount.")
        return   
    description = input("Description: ")
    category = input("Category: ")
    type = input("Type: ")
    if type not in ("Income","Expense"):
        print("Invalid transaction type")
        return
    transaction_id = str(uuid.uuid4())
    if type == "Income":
        balance += amount
    else:
        if(amount > balance):
            print("Insufficient Balance")
            return
        balance -= amount
    try:
        cursor.execute("BEGIN")
        
        # 1. Insert transaction
        cursor.execute(
            """
            INSERT INTO transactions("transaction_id", "amount", "category", "type","description", "balance", "acct_id") 
            VALUES(?,?,?,?,?,?,?)""", (transaction_id, amount, category, type, description, balance, acct_id) 
            )
        # 2. Update account balance
        cursor.execute(
            """
            UPDATE accounts
            SET acct_balance = ?
            WHERE id = ?
            """, (balance, acct_id)
            )             
        connection.commit()
        print(f"Transaction successful\nTransaction id: {transaction_id}\nNew Balance: {balance}")
    except Exception as e:
        connection.rollback()
        print(f"Transaction failed: {e}")

def view_all_transactions():
    cursor.execute("SELECT * FROM transactions")
    all_transactions = cursor.fetchall()
    if all_transactions == None:
        print("No transaction found")
        return
    print("(ID, Transaction_id, Amount, Category, Type, description, Balance)")
    for transaction in all_transactions:
        print(transaction)

def view_transaction():
    transaction_id = input("Enter the transaction id: ")
    cursor.execute("SELECT * FROM transactions WHERE transaction_id = ?", (transaction_id,))
    result = cursor.fetchone()
    if result == None:
        print("Transaction not Found")
        return
    transaction = result
    labels = [
        "ID",
        "Transaction ID",
        "Amount",
        "Category",
        "Type",
        "Description",
        "Balance after transaction"
    ]
    for index, value in enumerate(transaction):
        print(f"{labels[index]}: {value}")

def delete_transaction():
    transaction_id = input("Enter the transaction id: ")
    confirmation = input("Are you sure you want to delete this transaction (y/n): ")
    if confirmation == "y":
        cursor.execute("DELETE FROM transactions WHERE transaction_id = ?",(transaction_id, ))
        if cursor.rowcount == 0:
            print("Transaction not found")
        else: 
            print("deleting.....")
            print("Transaction deleted")
    elif confirmation == "n":
        print("Exited")
    else: print("Invalid option, exiting")

def clear_all_transaction():
    confirmation = input("Are you sure you want to clear all transaction? (y/n): ")
    if confirmation == "y":
        cursor.execute("DELETE FROM transactions")
        if cursor.rowcount == 0:
            print("No transactions to delete")
        else: 
            print("deleting.....")
            print("Transaction deleted")
    elif confirmation == "n":
        print("Exited")
    else: print("Invalid option, exiting")
    
def transaction_manager():
    print("""1. Add a new transaction.
2. View all transactions.
3. View a transaction.
4. Delete a transaction.
5. Delete all transactions.
""")
    choice = int(input("What would you like to do (Choose numbers 1-5)? "))
    if choice == 1:
        add_new_transaction()
    elif choice == 2:
        view_all_transactions()
    elif choice == 3:
        view_transaction()
    elif choice == 4:
        delete_transaction()
    elif choice == 5:
        clear_all_transaction()
    else:
        print("Invalid option")

transaction_manager()
connection.commit()
connection.close()
