def payoff(balance, mon_int, count, l_bound, u_bound):
    new_balance = balance
    amt = (l_bound + u_bound) / 2

    while (count < 12):
        count += 1
        new_balance = new_balance * (1 + mon_int) - amt

        if (new_balance <= 0 and u_bound - l_bound < 0.005):
            print("RESULT")
            print("{} {}".format("Monthly payment to pay off debt in 1 year: ", round(amt,2)))
            print("{} {}".format("Number of months needed: ", count))
            print("{} {}".format("Balance: ", round(new_balance, 2)))
            return

    if (new_balance > 0):
        payoff(balance, mon_int, 0, amt, u_bound)
    elif (new_balance < 0):
        payoff(balance, mon_int, 0, l_bound, amt)

balance = float(raw_input("Enter the outstanding balance on your credit card: "))
an_int = float(raw_input("Enter the annual credit card interest rate as a decimal: "))
mon_int = an_int / 12.0
count = 0
l_bound = balance / 12.0
u_bound = (balance*(1+(an_int/12))**12)/12
payoff(balance, mon_int, count, l_bound, u_bound)
