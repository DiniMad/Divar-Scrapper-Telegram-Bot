import pyotp

SECRET = pyotp.random_base32()


class OneTimePassword:
    def __init__(self):
        self.OtpObject = pyotp.TOTP(SECRET)

    def get_new_code(self):
        return self.OtpObject.now()

    def verify_code(self, code):
        return self.OtpObject.verify(code)
