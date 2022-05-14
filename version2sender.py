from shared import *

def make_header_v2(salt: str, difficulty: int, rcpt: str) -> str:
   static_header: bytes = f"X-Hashcash2: {salt}:{difficulty}:{rcpt}:".encode()
   nonce = 0
   while True:
      b64nonce = to_bytes(nonce)
      header = static_header + b64nonce
      digest = sha256(header)

      if bitstring(digest).count_starting_zeros() < difficulty:
         nonce += 1
         continue

      return header
