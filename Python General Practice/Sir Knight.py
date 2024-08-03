first_name = input("What is your first name? \n"
                   ":")
last_name = input("What is your last name? \n"
                  ":")
print(f"Greetings, {first_name.capitalize()} {last_name.capitalize()}, Sir Knight")
while True:
    isKnight = input(f"Sir {first_name.capitalize()}, you are a knight, arent you?:")
    if isKnight.lower().find("yes") != -1 or isKnight.lower() == "y":
        print("Well, then we are glad to have you in our lands!")
        break
    elif isKnight.lower().find("no") != -1 or isKnight.lower() == "n":
        print("To the gallows ye peasant!")
        break
    print("Speak up ye commoner. I cant hear yer!")
input()