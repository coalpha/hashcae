from typing import *
import hashlib
from base64 import b64encode as b64, b64decode as unb64
from random import randbytes

class bitstring:
   def __init__(self, bytes: bytes):
      self.bytes = bytes

   def __getitem__(self, idx: int) -> bool:
      byte = self.bytes[idx // 8]
      inner = idx % 8
      bitmask = 1 << inner
      return bool(byte & bitmask)

   def count_starting_zeros(self) -> int:
      count = 0
      while self[count] == False:
         count += 1
      return count

def sha256(s: bytes) -> bytes:
   return hashlib.sha256(s).digest()

def to_bytes(i: int) -> bytes:
   chunks = []
   while i:
      chunks.append((i % 64) + ord("A"))
      i //= 64
   return bytes(chunks)

from os import system
def cls(): system("cls")
