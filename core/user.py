from database import User
import secrets
import hashlib
import time


def getUser(userId):
    return User.objects(userId=userId).first()


def createUser(userName: str, email: str, password: str, timeShift: float = 0) -> str:
    userId = secrets.token_hex(8)
    while getUser(userId):
        userId = secrets.token_hex(8)

    salt = secrets.token_hex(16)
    passwordHash = hashlib.sha256(
        str(password + salt).encode('utf-8')).hexdigest()

    user = User(userId=userId, userName=userName, email=email,
                password=passwordHash, salt=salt, registerationTime=time.time(), timeShift=timeShift)
    try:
        user.save()
        return userId
    except:
        return None


def editUser(userId: str, properties: dict):
    protectedProperties = ['userId', 'status',
                           'tokens', 'salt', 'registerationTime']
    user = getUser(userId)
    if not user:
        return False

    # Protect those properties
    for key in protectedProperties:
        if key in properties:
            return False

    # Update status if email is in properties
    if 'email' in properties:
        properties['status'] = 'require-email-verification'

    # Update properties
    for key, value in properties.items():
        user[key] = value
    try:
        user.save()
        return True
    except:
        return False


def deleteUser(userId: str):
    user = getUser(userId)
    if not user:
        return False
    try:
        user.delete()
        return True
    except:
        return False


def getUserByEmail(email: str):
    return User.objects(email=email).first()

def getUserIdByEmail(email: str):
    user = getUserByEmail(email)
    if not user:
        return None
    return user.userId