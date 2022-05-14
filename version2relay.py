from shared import *
from datetime import datetime, timedelta

email = str
salt = str
expire_time = datetime

class invalidation_queue_entry:
   def __init__(self, expires: expire_time, sender: str, salt: str):
      self.expires = expires
      self.sender = sender
      self.salt = salt

class relay_salt_response:
   def __init__(self, b64salt: str, difficulty: int, expires: expire_time):
      self.b64salt = b64salt
      self.difficulty = difficulty
      self.expires = expires
   def __str__(self):
      return (""
         + f"relay_salt_response:\n"
         + f"   salt: {self.b64salt}\n"
         + f"   difficulty: {self.difficulty}\n"
         + f"   expires: {self.expires}"
      )

invalidation_queue: list[invalidation_queue_entry] = []
active_salts: dict[email, dict[salt, relay_salt_response]] = {}

def make_salt() -> str:
   return b64(randbytes(8)).decode()

active_time = timedelta(days=1)
def make_expire_time() -> expire_time:
   return datetime.now() + active_time

def get_salt(FROM: email, TO: email) -> relay_salt_response:
   # right now the TO field is not used in this relay server but it's part of
   # the protocol. it could be used to dynamically adjust the difficulty on a
   # per-user basis.
   if FROM not in active_salts:
      active_salts[FROM] = {}
   salt = make_salt()
   assert salt not in active_salts[FROM], "Somehow generated a duplicate salt oh no."
   # the difficulty increases the more active salts you have
   difficulty = 16 + int(len(active_salts[FROM])**.5)
   expire_time = make_expire_time()
   res = relay_salt_response(salt, difficulty, expire_time)
   active_salts[FROM][salt] = res
   invalidation_queue.append((expire_time, FROM, salt))
   return res

def relay_email(FROM: email, TO: email, header: str):
   "returns true if the email will be relayed"
   global invalidation_queue
   # first clean up old salts
   while invalidation_queue[0][0] < datetime.now():
      to_remove = invalidation_queue[0]
      del active_salts[to_remove.sender][to_remove.salt]
      invalidation_queue = invalidation_queue[1:]

   words = header.decode().split(":")
   assert len(words) == 5, "must be 5 words"
   assert words[0] == "X-Hashcash2", "wrong header name"
   assert words[1][0] == ' ', "should be space after header"
   salt = words[1][1:]
   difficulty = int(words[2])
   rcpt = words[3]
   print(f"{salt = }\n{difficulty = }\n{rcpt = }")
   assert active_salts[FROM][salt].difficulty == difficulty, "wrong minimum difficulty"
   assert TO == rcpt, f"recipient must match {TO}"
   digest = sha256(header)
   zeros = bitstring(digest).count_starting_zeros()
   print("hashing header")
   print(f"{zeros = }")
   assert difficulty <= zeros, "passed hash"
