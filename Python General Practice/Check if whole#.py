try:
    guess=int(input("Type a number:"))
except ValueError:
    print("This is not a whole number.")