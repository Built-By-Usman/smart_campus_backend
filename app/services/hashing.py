from pwdlib import PasswordHash
PasswordHash=PasswordHash.recommended()


def get_hashed_password(password):
    return PasswordHash.hash(password)

def verify_password(plainPassword,hashedPassword):
    return PasswordHash.verify(plainPassword,hashedPassword)