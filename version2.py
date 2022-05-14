from shared import cls
from time import sleep
import version2sender as sender
import version2relay as relay

cls()
print("You are the sender now.")
print("What is your email?")
semail = input("sender> ")

print("Who are you emailing?")
srcpt = input("sender> ")

def dot():
   print(end=".", flush=True)

def ddd():
   sleep(.7); dot()
   sleep(.7); dot()
   sleep(.7); dot()
   sleep(.7); dot()
   sleep(.7); dot()
   sleep(.7); dot()
   cls()

print(f"from = {semail}")
print(f"to   = {srcpt}")
print("Sending to the relay server")
print("---------")
print("You are the relay server now.")
print(f"Generating an email id / salt for {semail} -> {srcpt}")
res = relay.get_salt(semail, srcpt)
print(res)
print("Returning to the sender")
print("---------")

print("You are the sender now.")
print("Making the header.")
header = sender.make_header_v2(res.b64salt, res.difficulty, srcpt)
print(header)
print("Sending the email")
print("---------")

print("You are the relay server now.")
print(f"Got {header}")
relay.relay_email(semail, srcpt, header)
print("Passed!")
