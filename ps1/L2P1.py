def cc_payment(balance, interest, mininmum, total_paid, count):
    min_pay = round(mininmum * balance, 2)
    int_paid = round((interest / 12.0) * balance, 2)
    princ_paid = round(min_pay - int_paid, 2)
    balance = round(balance - princ_paid, 2)
    total_paid += princ_paid + int_paid

    print("{} {} ".format("Month: ", count))
    print("{} {} ".format("Minimum monthly payment: ", min_pay))
    print("{} {} ".format("Principle paid: ", princ_paid))
    print("{} {} ".format("Remaining balance: ", balance))
    count += 1

    if (count <= 12):
        cc_payment(balance, interest, mininmum, total_paid, count)
    else:
        print("RESULT")
        print("{} {}".format("Total amount paid: ", total_paid))
        print("{} {}".format("Remaining balance: ", balance))

balance = float(raw_input("Enter the outstanding balance on your credit card: "))
interest = float(raw_input("Enter the annual credit card interest rate as a decimal: "))
mininmum = float(raw_input("Enter the minimum monthly payment rate as a decimal: "))
total_paid = 0
count = 1

cc_payment(balance, interest, mininmum, total_paid, count)
