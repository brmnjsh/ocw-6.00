def payoff(balance, mon_int, count, amt):
    new_balance = balance
    while (count < 12):
        count += 1
        new_balance = round(new_balance * (1 + mon_int) - amt, 2)

        if (new_balance <= 0):
            print("RESULT")
            print("{} {}".format("Monthly payment to pay off debt in 1 year: ", amt))
            print("{} {}".format("Number of months needed: ", count))
            print("{} {}".format("Balance: ", new_balance))
            return

    if (new_balance > 0):
        payoff(balance, mon_int, 0, amt + 10)

balance = float(raw_input("Enter the outstanding balance on your credit card: "))
an_int = float(raw_input("Enter the annual credit card interest rate as a decimal: "))
mon_int = an_int / 12.0
count = 0
amt = 10
payoff(balance, mon_int, count, amt)
