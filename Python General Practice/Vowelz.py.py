while True:
      letter = input("Give an example of a vowel:")
      vowels_string = ("aeiou")#STRING
      #vowels_set = {"a,"e", "i", "o", "u"}
      #vowel_list = ["a,"e", "i", "o", "u"]
      #vowel_tuple = ("a,"e", "i", "o", "u")
      #vowel_dict = {"a: "apple", "e": "elephant", "I": "impala", "o": "ocelot",
      #"u": "unicorn"}
      if letter.lower() in vowels_string:
            print("That is a vowel, very good.")
            break
      else:
            print("Try again if you want, no rush.. idiot")
input()