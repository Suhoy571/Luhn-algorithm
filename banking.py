import random
import sqlite3


class Card:
    conn = sqlite3.connect('card.s3db')

    cur = conn.cursor()
    card_pin = 0
    card_number = 0
    balance = 0

    def create_account(self):
        while True:
            self.card_number = int("400000" + str(''.join([str(random.randint(0, 9)) for _ in range(10)])))
            if self.luhn_algorithm(self.card_number):
                break
        self.card_pin = ''.join([str(random.randint(0, 9)) for _ in range(4)])
        self.balance = 0
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS card  (  id INTEGER PRIMARY KEY autoincrement , "
            " number TEXT,  pin TEXT,  balance INTEGER DEFAULT 0);")
        self.cur.execute("INSERT INTO card (number, pin, balance) values (?, ?, ?)",
                         (self.card_number, self.card_pin, self.balance))
        self.conn.commit()

    def __init__(self):
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS card  (  id INTEGER PRIMARY KEY autoincrement , "
            " number TEXT,  pin TEXT,  balance INTEGER DEFAULT 0);")
        self.conn.commit()

    def login(self, number, pin):
        self.cur.execute(f"SELECT * FROM card WHERE pin = {pin} and number = {number}")
        account = self.cur.fetchall()
        try:
            if account[0][1] == str(number) and account[0][2] == str(pin):
                print('\nYou have successfully logged in!\n')
                return True
            else:
                print("\nWrong card number or PIN!\n")
                return False
        except:
            return False

    def get_customer_balance(self, number, pin):
        self.cur.execute(f"SELECT balance FROM card WHERE pin = {pin} and number = {number};")
        balance = self.cur.fetchall()
        self.balance = balance[0][0]
        return self.balance

    def add_income(self, pin, number, value):
        self.cur.execute(f"SELECT balance FROM card WHERE pin = {pin} and number = {number};")
        current_balance = self.cur.fetchall()
        new_balance = int(current_balance[0][0]) + int(value)
        self.cur.execute(f"UPDATE card SET balance = {new_balance} WHERE pin = {pin} and number = {number};")
        self.conn.commit()

    def do_transfer(self, card_number, card_transfer, money_to_transfer):
        self.cur.execute(f"SELECT balance FROM card WHERE number = {card_number};")
        current_balance = self.cur.fetchall()
        self.cur.execute(f"SELECT balance FROM card WHERE number = {card_transfer};")
        transfer_to_balance = self.cur.fetchall()
        if int(current_balance[0][0]) < int(money_to_transfer):
            return "Not enough money!\n"
        else:
            balance = int(transfer_to_balance[0][0]) + (int(current_balance[0][0]) - int(money_to_transfer))
            self.cur.execute(f"UPDATE card SET balance = {balance} WHERE number = {card_transfer};")
            self.cur.execute(
                f"UPDATE card SET balance = {int(current_balance[0][0]) - int(money_to_transfer)} WHERE number = {card_number};")
            self.conn.commit()
            return "Success!\n"

    def close_account(self, number, pin):
        self.cur.execute(f"DELETE FROM card WHERE pin = {pin} and number = {number};")
        self.conn.commit()

    def check_if_card_exist(self, number):
        self.cur.execute(f"SELECT * FROM card WHERE number = {number};")
        card = self.cur.fetchall()
        if card:
            return True
        else:
            return False

    def get_all_data(self):
        self.cur.execute("SELECT * FROM card;")
        data = self.cur.fetchall()
        for i in data:
            print(i)
        print()

    def luhn_algorithm(self, card_number):
        multi_card_number = []
        for i, value in enumerate(str(card_number)[:-1]):
            if i % 2 == 0:
                value = int(value) * 2
                if int(value) > 9:
                    value = int(value) - 9
                    multi_card_number.append(value)
                else:
                    multi_card_number.append(value)
            else:
                multi_card_number.append(value)
        if (sum([int(k) for k in multi_card_number]) + int(str(card_number)[-1])) % 10 == 0:
            return True
        else:
            return False


while True:
    menu = input("1. Create an account\n2. Log into account\n0. Exit\n")
    customer = Card()
    if menu == "1":
        customer.create_account()
        print("\nYour card has been created")
        print(f"Your card number: \n{customer.card_number}")
        print(f"Your card PIN: \n{customer.card_pin}\n")
    if menu == "2":
        card_number = int(input("Enter your card number:\n"))
        pin = int(input("Enter your PIN:\n"))
        if customer.login(card_number, pin):
            while True:
                menu = input("1. Balance\n2. Add income\n"
                             "3. Do transfer\n4. Close account\n5. Log out\n0. Exit\n")
                if menu == "1":
                    print(f"\nBalance: {customer.get_customer_balance(card_number, pin)} \n")
                if menu == "2":
                    customer.add_income(pin, card_number, input('Enter income: \n'))
                    print("Income was added!\n")
                if menu == "3":
                    print('\nTransfer')
                    card_to_transfer = input('Enter card number: \n')
                    if card_to_transfer == card_number:
                        print("You can't transfer money to the same account!\n")
                        continue
                    if customer.luhn_algorithm(card_to_transfer):
                        if customer.check_if_card_exist(card_to_transfer):
                            print(customer.do_transfer(card_number, card_to_transfer,
                                                       input('Enter how much money you want to transfer: \n')))
                        else:
                            print("Such a card does not exist.\n")
                    else:
                        print("Probably you made a mistake in the card number. Please try again!\n")

                if menu == "4":
                    customer.close_account(number=card_number, pin=pin)
                    print("The account has been closed!\n")
                    break
                if menu == "5":
                    print("\nYou have successfully logged out!\n")
                    break
                if menu == "0":
                    break
        else:
            print("Wrong card number or PIN!\n")
    if menu == "8":
        customer.get_all_data()
    if menu == "0":
        print("\nBye!")
        break
