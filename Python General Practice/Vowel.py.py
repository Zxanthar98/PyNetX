while True:
      letter = input("Give an example of a vowel:")
      vowels = ("aeiou")
      if letter.lower() in vowels:
            print("That is a vowel, very good.")
            break
      else:
            print("Try again if you want, no rush.. idiot")
input()