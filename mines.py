import random
import sqlite3

MAX_MINES = 5
MAX_BET_AMOUNT = 500
MIN_BET_AMOUNT = 1

ROWS = 5
COLS = 5

MINES_POFIT_CHART = {1: 1.25, 2: 1.5, 3: 2, 4: 5, 5: 10}

DIAMOND = "💚"
MINE = "💣"


def deposit():
    while True:
        print()
        amount = input("What is your deposite amount? ₹")
        if amount.isdigit():
            amount = int(amount)
            if amount > 0:
                print("\nTransaction successful.")
                break
            else:
                print("\nSorry, can't deposite amount ₹0")
                break
        else:
            print("Please enter a valid number.")

    return amount


def get_number_of_mines():
    while True:
        print()
        mines = input(
            "Enter the number of mines to bet on (1-" + str(MAX_MINES) + ") : "
        )
        if mines.isdigit():
            mines = int(mines)
            if 1 <= mines <= MAX_MINES:
                break
            else:
                print("Lises must be from 1 to " + str(MAX_MINES))
        else:
            print("Please enter a valid number.")
    return mines


def get_bet_amount():
    while True:
        print()
        amount = input(
            f"What would be the bet amount (₹{MIN_BET_AMOUNT} - ₹{MAX_BET_AMOUNT}) ₹"
        )
        if amount.isdigit():
            amount = int(amount)
            if MIN_BET_AMOUNT <= amount <= MAX_BET_AMOUNT:
                break
            else:
                print(
                    f"Enter any amount between (₹{MIN_BET_AMOUNT} - ₹{MAX_BET_AMOUNT}."
                )
        else:
            print("Enter a valid number.")
    return amount


def get_choices(row, col, mines):
    choices = []

    for _ in range(mines):
        choices.append(MINE)

    for _ in range((row * col) - mines):
        choices.append(DIAMOND)

    return choices


def get_mines_spin(choices):
    choices = choices[:]
    spin = []

    for _ in range(ROWS):
        row = []
        for _ in range(COLS):
            i = random.choice(choices)
            row.append(i)
            choices.remove(i)
        spin.append(row)

    return spin


def printSpin(spin):
    print()
    for i in spin:
        for j in i:
            print(j, end=" ")
        print()


def select_row_column():
    while True:
        print()
        line = input("What do want to select between row and column(r/c): ").lower()
        if line == "c" or line == "r":
            break
        else:
            print("Invalid choice entered.")

    while True:
        print()
        if line == "r":
            row = input(f"Select the row(1-{ROWS}): ")
            if row.isdigit():
                row = int(row)
                if 1 <= row <= ROWS:
                    col = None
                    row -= 1
                    break
                else:
                    print(f"Please select a valid row between(1-{ROWS}).")
            else:
                print("Please enter valid number values.")
        else:
            col = input(f"Select the column(1-{COLS}): ")
            if col.isdigit():
                col = int(col)
                if 1 <= col <= ROWS:
                    row = None
                    col -= 1
                    break
                else:
                    print(f"Please select a valid row between(1-{COLS}).")
            else:
                print("Please enter valid number values.")
    return row, col


def isWinner(spin, row, col):
    if row != None:
        if spin[row].count(MINE):
            return False
    else:
        for i in spin:
            if i[col] == MINE:
                return False

    return True


def play(balance):
    print()
    print("➖"*10)
    print("mines    profit")
    for mines, profit in MINES_POFIT_CHART.items():
        print(f"  {mines}       {profit}x")
    print("➖"*10)

    mines = get_number_of_mines()
    while True:
        bet_amount = get_bet_amount()

        if bet_amount > balance:
            print(f"Insufficient balance. Your balance is ₹{balance}")
        else:
            break

    row, col = select_row_column()
    # print(f"row = {row}, col = {col}")

    balance = balance - bet_amount

    choices = get_choices(ROWS, COLS, mines)
    spin = get_mines_spin(choices)

    printSpin(spin)
    print("\n 〰️〰️〰️〰️ RESULT 〰️〰️〰️〰️")
    if isWinner(spin, row, col):
        profit = bet_amount * MINES_POFIT_CHART[mines]
        balance = balance + profit
        print("\n🎉🎉🥳PROFIT🥳🎉🎉")
        print(f" Bet: {bet_amount}")
        print(f" Profit:{profit - bet_amount} ({MINES_POFIT_CHART[mines]}x)")
        print(f" Balance: ₹{balance}")
    else:
        print("\n🥺🥺🥺LOSS🥺🥺🥺")
        print(f" Bet: {bet_amount}")
        print(f" Loss:{bet_amount}")
        print(f" Balance: ₹{balance}")

    return balance


def main():
    print(f"{"〰️"*20} WELCOME TO THE MINES {"〰️"*20}")

    balance = 0

    connection  = sqlite3.connect("acccount.db")
    
    cursor = connection.cursor()
    
    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS account(
            balance REAL
        )
        '''
    )
    
    connection.commit()
    
    cursor.execute("SELECT COUNT(*) FROM account")
    
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO account (balance) VALUES (?)",(balance,))
        connection.commit()
    
    cursor.execute("SELECT balance FROM account")
    
    balance = cursor.fetchone()[0]
    
    while True:
        print()
        print("➖" * 50)
        print("\n********** CHOICES *********")
        print(
            f"\n1. See your baance\n2. Deposite money\n3. Play game\n4. Exit the app"
        )
        
        choice = input("\nEnter your choice: ")
        
        match choice:
            case '1':
                print(f"\nYour balance is : ₹{balance}")
            case '2':
                balance = balance + deposit()
                cursor.execute("UPDATE account SET balance = ?",(balance,))
                connection.commit()
            case '3':
                if balance > 0:
                    balance = play(balance)
                    cursor.execute("UPDATE account SET balance = ?",(balance,))
                    connection.commit()
                else:
                    print("Low balance.")
            case '4':
                connection.close()
                break
            case _:
                print("Enter a valid choice.")


if __name__ == "__main__":
    main()
