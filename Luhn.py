import random


class Card:
    def __init__(self):
        self.card_number = int("400000" + str(random.randrange(0000000000, 9999999999)))
        self.card_pin = random.randrange(0000, 9999)
        self.balance = 0

    def login(self, number, pin):
        if self.card_number == number and self.card_pin == pin:
            print('\nYou have successfully logged in!\n')
            return True
        elif self.card_number != number or self.card_pin != pin:
            print("\nWrong card number or PIN!\n")
            return False

    def get_balance(self):
        return self.balance


while True:
    menu = input("1. Create an account\n2. Log into account\n0. Exit\n")
    global customer
    if menu == "1":
        customer = Card()
        print("\nYour card has been created")
        print(f"Your card number: \n{customer.card_number}")
        print(f"Your card PIN: \n{customer.card_pin}\n")
    if menu == "2":
        result = customer.login(int(input("Enter your card number:\n")), int(input("Enter your PIN:\n")))
        if result:
            while True:
                menu = input("1. Balance\n2. Log out\n0. Exit\n")
                if menu == "1":
                    print(f"\nBalance: {customer.balance} \n")
                if menu == "2":
                    print("\nYou have successfully logged out!\n")
                    break
                if menu == "0":
                    break
    if menu == "0":
        break
