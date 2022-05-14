# hashcæ

### version1

- no scaling of difficulty with amount of spam emails
- no way for email rcpt to require higher difficulty
- hashes can be computed ahead of time and then spammed later

`X-Hashcash: <version = 1>:<difficulty = 20>:<date>:<email>::<random>:<nonce>`

```mermaid
sequenceDiagram
Sender ->> Hashcash V1: difficulty, date, email recipient
loop Proof of Work
   Hashcash V1 ->> Hashcash V1: hash header
end
Hashcash V1 ->> Sender: X-Hashcash: 1:16:2022.05.14:email@example.com::ljyQKNT+Gxw=:xNz
Sender ->> Recipient: Send Email
```

### version2

`X-Hashcash2: <salt>:<difficulty>:<recipient email>:<nonce>`

```mermaid
sequenceDiagram
participant Sender
participant Hashcash V2
participant Relay Server
participant Recipient
Sender ->> Relay Server: sender's email, email recipient
Relay Server ->> Sender: salt, difficulty
Sender ->> Hashcash V2: difficulty, salt from server, recipient
loop Proof of Work
   Hashcash V2 ->> Hashcash V2: hash header
end
Hashcash V2 ->> Sender: X-Hashcash2: <difficulty>:<recipient email>:<salt>:<nonce>
Sender ->> Relay Server: header
Relay Server ->> Recipient: relays email after verification
```
