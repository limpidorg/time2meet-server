import logger
from database import User, Token, PlannerPermission, OTP
import core.user
import core.planner
import time
import secrets
import hashlib

from emaillib.templates.general import GeneralEmail, OTPEmail
import emaillib.core


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
        logger.debug(f"Verifying token {token} of user {userId}.")
        for t in user.tokens:
            if t.token == token and t.expires > time.time():
                logger.info(f"Token {token} of user {userId} is valid.")
                return AuthResult(True, 0, userId, t.scopes)
        logger.warning(f"Token {token} of user {userId} is invalid.")
        return AuthResult(False, -101)
    logger.warning(f"User {userId} is not found.")
    return AuthResult(False, -200)


def _cleanExpiredTokens(user):
    logger.debug(f"Cleaning up expired tokens for user {user.userId}")
    for t in user.tokens:
        if t.expires <= time.time():
            user.tokens.remove(t)
            logger.debug(f"Removed expired token {t.token}")
    try:
        user.save()
    except:
        pass


def _cleanExpiredOTP():
    for entry in OTP.objects():
        if entry.expires <= time.time():
            entry.delete()


def verifyPassword(userId, password):
    logger.debug(f"Verifying password for user {userId}.")
    user = core.user.getUser(userId)
    if user:
        salt = user.salt
        passwordHash = hashlib.sha256(
            str(password + salt).encode('utf-8')).hexdigest()
        if user.password == passwordHash:
            logger.info(f"Password for user {userId} is valid.")
            return AuthResult(True, 0, userId)
        logger.warning(f"Password for user {userId} is invalid.")
        return AuthResult(False, -103)
    logger.warning(f"User {userId} is not found.")
    return AuthResult(False, -200)


def getUserPlannerPermission(userId, plannerId):
    return PlannerPermission.objects(userId=userId, plannerId=plannerId).first()


def plannerPermission(permission, plannerId, userId=None):
    planner = core.planner.getPlanner(plannerId)
    if planner:
        logger.debug(
            f"Checking permission {permission} for planner {plannerId}")
        # Checks for planner public permissions.
        if permission in planner.permissions:
            logger.info(f"Permission {permission} is available to the public.")
            return AuthResult(True, 0)
        # Checks if the user is the creator
        if planner.createdBy == userId:
            logger.info(
                f"User {userId} is the creator of planner {plannerId}.")
            return AuthResult(True, 0)
    else:
        logger.warning(f"Planner {plannerId} is not found.")
        return AuthResult(False, -300)

    # Checks for planner private permissions.
    logger.debug(
        f"Checking private permission: {permission} for planner {plannerId}, user {userId}")
    if userId:
        plannerPermission = getUserPlannerPermission(userId, plannerId)
        if plannerPermission:
            if permission in plannerPermission.permissions:
                logger.info(
                    f"User {userId} has permission {permission} for planner {plannerId}.")
                return AuthResult(True, 0)  # User-specific permission
    logger.warning(
        f"User {userId} does not have permission {permission} for planner {plannerId}.")
    return AuthResult(False, -105, message=f"Access is denied: userId of {str(userId) if userId else '<PUBLIC>'} do not have the {permission} permission to access the requested resource.")


def updateUserPlannerPermissions(userId, plannerId, permissions=[]):
    logger.debug(
        f"Updating permissions for user {userId}, planner {plannerId} to {str(permissions)}...")
    if not core.planner.getPlanner(plannerId):
        return False
    if not core.user.getUser(userId):
        return False

    plannerPermission = getUserPlannerPermission(userId, plannerId)
    if plannerPermission:
        if permissions == []:
            plannerPermission.delete()
            logger.info(
                f"Removed permissions for user {userId}, planner {plannerId}.")
            return True
        plannerPermission.permissions = permissions
        try:
            plannerPermission.save()
            logger.info(
                f"Updated permissions for user {userId}, planner {plannerId}")
            return True
        except:
            return False
    else:
        plannerPermission = PlannerPermission(
            userId=userId, plannerId=plannerId, permissions=permissions)
        try:
            plannerPermission.save()
            logger.info(
                f"Created new planner permission for user {userId}, planner {plannerId}")
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
            logger.info(f"Generated token {token} for user {userId}.")
            return token
        except Exception as e:
            raise
            return None
    return None


def getTokenInfo(userId, token) -> dict:
    logger.debug(f"Getting token info for user {userId} and token {token}")
    user = core.user.getUser(userId)
    if user:
        _cleanExpiredTokens(user)
        for t in user.tokens:
            if t.token == token and t.expires > time.time():
                logger.info(f"Got token info. token={token}, user={userId}.")
                return t
        logger.warning(f"Token {token} does not exist (user={userId}).")
        return None
    logger.warning(f"User {userId} is not found.")
    return None


def deleteToken(userId, token):
    user = core.user.getUser(userId)
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


def generateOTP(userId, permission='verify-identity'):
    user = core.user.getUser(userId)
    if user:
        otp = secrets.token_hex(3).upper()
        otpEntry = OTP(userId=userId, otp=otp,
                       expires=time.time() + 600, permission=permission)
        try:
            otpEntry.save()
            logger.info(f"Generated OTP {otp} for user {userId}.")
            return otp
        except:
            return None
    return None


def verifyOTP(userId, otp, permission='verify-identity'):
    user = core.user.getUser(userId)
    if user:
        _cleanExpiredOTP()
        for otpEntry in OTP.objects(userId=userId):
            if otpEntry.otp == otp and otpEntry.expires > time.time() and otpEntry.permission == permission:
                otpEntry.delete()
                logger.info(f"Verified OTP {otp} for user {userId}.")
                return True
        logger.warning(f"Invalid OTP {otp} for user {userId}.")
        return False
    logger.warning(f"User {userId} is not found.")
    return False


def sendEmailOTP(userId, permission='verify-email'):
    logger.debug(f"Sending OTP to user {userId}...")
    user = core.user.getUser(userId)
    if user:
        otp = generateOTP(userId, permission=permission)
        if otp:
            if emaillib.core.sendEmail(OTPEmail, email=user.email, subject="Verify your email address", name=user.userName, code=otp, permission=permission):
                logger.info(f"OTP {otp} is sent to user {userId}.")
                return otp
            else:
                logger.warning(
                    f"Failed to send email to {user.email} ({userId})")
                return None
        else:
            logger.error("Failed to generate OTP")
            return None
