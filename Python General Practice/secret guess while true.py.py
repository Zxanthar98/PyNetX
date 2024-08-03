import random
while True:
      guess=int(input("Type a number between 1-10:"))
      secret=(random.randint(1,11))
      diff=guess-secret
      if diff==0:
            print("On the money, big man")
            break
      elif guess>secret:
               print("Too high")         
      elif guess<secret:
            print("Too low")
input()