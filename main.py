import uuid
from datetime import datetime
from database import get_connection

connection = get_connection()
cursor = connection.cursor()

class All_transactions:
    def __init__(self, amount, type, description, category, balance):
        self.transaction_id = str(uuid.uuid4())
        self.amount = amount
        self.type = type
        self.description = description
        self.category = category
        self.balance = balance

    def income_transaction(self):
        print(self.balance)
        if(self.amount < 0):
            return("Invalid amount")
        else:
            self.balance += self.amount
            print(f"Deposit successful\nTransaction id: {self.transaction_id}\nNew Balance: {self.balance}")
            cursor.execute("""
                INSERT INTO transactions("transaction_id", "amount", "category", "type","description", "balance") 
                VALUES(?,?,?,?,?,?)""", (self.transaction_id, self.amount, self.category, self.type, self.description, self.balance) 
                )
            return(self.balance)

    def expense_transaction(self): 
        if(self.amount > self.balance):
            return("Insufficient Balance")
        elif(self.amount < 0):
            return("Invalid transaction amount")
        else:
            self.balance -= self.amount
            print(f"Deposit successful\nTransaction id: {self.transaction_id}\nNew Balance: {self.balance}")
            cursor.execute("""
                            INSERT INTO transactions("transaction_id", "amount", "category", "type","description", "balance") 
                            VALUES(?,?,?,?,?,?)""", (self.transaction_id, self.amount, self.category, self.type, self.description, self.balance) 
                            )
                        
            return(self.balance)




def create_transaction():
    transaction_count = 0;
    amount = int(input("Amount: "))
    description = input("Description: ")
    category = input("Category: ")
    type = input("Type: ")
    acct_name = input("Acct_name: ")
    cursor.execute("SELECT acct_balance FROM accounts where acct_name = ? ", (acct_name,))
    balance = cursor.fetchone
    if(type == "Income"):
        transaction_count += 1
        transaction_name = f"transc{str(transaction_count)}" 
        transaction_name = All_transactions(amount, type, description, category, balance)
        balance = transaction_name.income_transaction()
        cursor.execute(
                        """
                        INSERT INTO accounts(acct_name, acct_balance) VALUES(?,?)
                        ON CONFLICT(acct_name)
                        DO UPDATE SET
                        acct_balance = excluded.acct_balance
                        """, (acct_name, balance)
                        )
    elif(type == "Expense"):
        transaction_count += 1
        transaction_name = f"transc{str(transaction_count)}" 
        transaction_name = All_transactions(amount, type, description, category)
        balance = transaction_name.expense_transaction()
        
    else: print("Invalid transaction type")
    

create_transaction()
connection.commit()
connection.close()