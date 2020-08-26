import sys
import bcrypt
from datetime import datetime
from .attestationdb import AttestationDB
from binascii import hexlify, unhexlify
import random
import string
import pyotp

class User(AttestationDB):
    def __init__(self):
        AttestationDB.__init__(self)
        self.user_id = None
        self.name = None
        self.salt = None
        self.pwdhash = None
        self.lastlogin = None
        self.whenadded = None

    def addUser(self, username, password):
        #check if user exists already, return False if it does
        if self.checkUserName(username):
            return False
        
        dateTimeObj = datetime.now()
        timestampStr = dateTimeObj.strftime("%Y%m%d%H%M%S%w")
        
        salt = bcrypt.gensalt(rounds=16)
        hashed_pwd = bcrypt.hashpw(password.encode('utf8'), salt)
        otpsecret = pyotp.random_base32()
        
        sql_query = 'INSERT INTO user(name, salt, pwdhash, whenadded, otpsecret) ' \
                    'VALUES(%s, %s, %s, %s, %s);'
        
        sql_data = (username, hexlify(salt).decode('ascii'), hexlify(hashed_pwd).decode('ascii'), timestampStr, otpsecret)
        
        try:
            self.query(sql_query, sql_data)
            return True
        except:
            print("User add "+username+" exception:", sys.exc_info()[0])
            return False
        else:
            return False
        
    def validateUser(self, username, password):
        sql_query = """SELECT * FROM user WHERE name=%s;"""
        sql_data = (username,)
        
        result = self.query(sql_query, sql_data)
        
        if result:
            rows = result.fetchall()
            
            if len(rows) == 0:
                return False
            
            salt = unhexlify(rows[0]['salt'])
            pwdhash = unhexlify(rows[0]['pwdhash'])
            
            hashed_pwd = bcrypt.hashpw(password.encode('utf8'), salt)
            
            if pwdhash == hashed_pwd:
                return True
            
        else:
            print("Error occured")
            
        return False

    def checkUserName(self, username):
        sql_query = """SELECT * FROM user WHERE name=%s;"""
        sql_data = (username,)
        
        print("checkUserName sql:",sql_query, sql_data)
        
        result = self.query(sql_query, sql_data)
        
        if result:
            rows = result.fetchall()
            
            print("row count is ",len(rows))
            
            if len(rows) > 0:
                return True
        else:
            print("Error occured")
            
        return False
    
    def getOtpSecret(self, username):
        sql_query = """SELECT otpsecret FROM user WHERE name=%s;"""
        sql_data = (username,)
                
        result = self.query(sql_query, sql_data)
        
        if result:
            rows = result.fetchall()
            
            print("row count is ",len(rows))
            
            if len(rows) > 0:
                return rows[0]['otpsecret']
        else:
            print("Error occured")
            
        return None
    
    def getRandomString(self, length):
        letters_and_digits = string.ascii_letters + string.digits
        result_str = ''.join((random.choice(letters_and_digits) for i in range(length)))
        return result_str
