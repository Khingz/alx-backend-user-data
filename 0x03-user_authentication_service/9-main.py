#!/usr/bin/env python3

from auth import Auth

email = 'bob@bob.com'
password = 'MyPwdOfBob'
auth = Auth()

auth.register_user(email, password)
print(auth.get_reset_password_token(email))
