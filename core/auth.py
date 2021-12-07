from database import User, Token
import core.user
import time
import secrets
import hashlib


class AuthResult():
    def __init__(self, succeeded, code, userId=None, scopes=[], message=None, data=None):
        self.succeeded = succeeded
        self.code = code
        self.userId = userId
        self.scopes = scopes
        self.message = message
        self.data = data

    def __bool__(self):
        return self.succeeded


def verifyToken(userId, token) -> AuthResult:
    user = core.user.getUser(userId)
    if user:
        # Clean expired tokens & tidy up the database.
        # Note: This function is not technically a part of verifyToken.
        # It does not improve the security etc - it simply cleans up the database.
        _cleanExpiredTokens(user)
        for t in user.tokens:
            if t.token == token and t.expires > time.time():
                return AuthResult(True, 0, userId, t.scopes)
        return AuthResult(False, -101)
    return AuthResult(False, -200)


def _cleanExpiredTokens(user):
    for t in user.tokens:
        if t.expires <= time.time():
            user.tokens.remove(t)
    try:
        user.save()
    except:
        pass


def verifyPassword(userId, password):
    user = core.user.getUser(userId)
    if user:
        salt = user.salt
        passwordHash = hashlib.sha256(
            str(password + salt).encode('utf-8')).hexdigest()
        if user.password == passwordHash:
            return AuthResult(True, 0, userId)
        return AuthResult(False, -103)
    return AuthResult(False, -200)


def login(email, password) -> AuthResult:
    userId = core.user.getUserIdByEmail(email)
    if userId:
        return verifyPassword(userId, password)
    return AuthResult(False, -200)


def generateToken(userId, maxAge=86400 * 7, scopes=[]) -> str:
    user = core.user.getUser(userId)
    if user:
        token = secrets.token_hex(32)
        user.tokens.append(
            Token(token=token, expires=time.time() + maxAge, scopes=scopes))
        try:
            user.save()
            return token
        except Exception as e:
            raise
            return None
    return None
