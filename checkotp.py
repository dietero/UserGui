import pyotp
import sys
from database.dbuser import User 

if len(sys.argv) == 0:
    print('Usage: python3 checkotp.py <username>')
    sys.exit()
    
user = User()
secret = user.getOtpSecret(sys.argv[1])

if secret is None:
    print('User '+sys.argv[1]+' does not exist')
    sys.exit(1)
    
otp = pyotp.TOTP(secret)
print("Current OTP: ", otp.now())