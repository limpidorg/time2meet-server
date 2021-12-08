from database import User, Token, PlannerPermission
import core.user
import core.planner
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


def getUserPlannerPermission(userId, plannerId):
    return PlannerPermission.objects(userId=userId, plannerId=plannerId).first()


def plannerPermission(permission, plannerId, userId=None):
    planner = core.planner.getPlanner(plannerId)
    if planner:
        # Checks for planner public permissions.
        if permission in planner.permissions:
            return AuthResult(True, 0)
        # Checks if the user is the creator
        if planner.createdBy == userId:
            return AuthResult(True, 0)
    else:
        return AuthResult(False, -300)

    # Checks for planner private permissions.
    if userId:
        plannerPermission = getUserPlannerPermission(userId, plannerId)
        if plannerPermission:
            if permission in plannerPermission.permissions:
                return AuthResult(True, 0)  # User-specific permission

    return AuthResult(False, -105, message=f"Access is denied: userId of {str(userId) if userId else '<PUBLIC>'} do not have the {permission} permission to access the requested resource.")


def updateUserPlannerPermissions(userId, plannerId, permissions=[]):
    if not core.planner.getPlanner(plannerId):
        return False
    if not core.user.getUser(userId):
        return False

    plannerPermission = getUserPlannerPermission(userId, plannerId)
    if plannerPermission:
        if permissions == []:
            plannerPermission.delete()
            return True
        plannerPermission.permissions = permissions
        try:
            plannerPermission.save()
            return True
        except:
            return False
    else:
        plannerPermission = PlannerPermission(
            userId=userId, plannerId=plannerId, permissions=permissions)
        try:
            plannerPermission.save()
            return True
        except:
            return False


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


def getToken(uID, token) -> dict:
    user = core.user.getUser(uID)
    if user:
        _cleanExpiredTokens(user)
        for t in user.tokens:
            if t.token == token and t.expires > time.time():
                return t
        return None
    return None


def deleteToken(uID, token):
    user = core.user.getUser(uID)
    if user:
        _cleanExpiredTokens(user)
        for t in user.tokens:
            if t.token == token:
                user.tokens.remove(t)
                try:
                    user.save()
                    return True
                except Exception as e:
                    return False
        return False
    return False
