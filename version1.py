from shared import *

def make_header_v1(bits: int, date: str, rcpt: str):
   rand0 = b64(randbytes(8))
   static_header = f"X-Hashcash: 1:{bits}:{date}:{rcpt}::".encode()
   counter = 0
   while True:
      b64counter = to_bytes(counter)
      header = static_header + rand0 + b":" + b64counter
      digest = sha256(header)
      if bitstring(digest).count_starting_zeros() >= bits:
         return header
      else:
         counter += 1

z = int(input("How many zeros?\n> "))
d = input("What's the date to send it on?\n> ")
e = input("Who is the email to?\n> ")

print(make_header_v1(z, d, e))
