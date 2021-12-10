from RequestMap.Validators.ValidatorBase import StandardValidator, ValidationError
import core.auth
import core.planner
import logger


class AuthenticationValidator(StandardValidator):
    def __init__(self):
        super().__init__()
        self.AUTHENTICATION_METHODS = {
            'verify-token': self.verifyToken,
            'verify-password': self.verifyPassword,
            'login': self.login,
            'public': lambda: None  # No authentication required
        }

    def verifyToken(self, userId, token):
        authResult = core.auth.verifyToken(userId, token)
        if not authResult.succeeded:
            raise ValidationError(authResult.code, authResult.message)

    def verifyPassword(self, userId, password):
        authResult = core.auth.verifyPassword(userId, password)
        if not authResult.succeeded:
            raise ValidationError(authResult.code, authResult.message)

    def login(self, email, password):
        authResult = core.auth.login(email, password)
        if not authResult.succeeded:
            raise ValidationError(authResult.code, authResult.message)

    def noAuthenticationMethodIsAvailable(self):
        raise ValidationError(-100)  # No authentication method is available

    def getEvaluationMethod(self, endpoint, protocolName):
        if 'authlevel' in endpoint['metadata']:
            authLevel = endpoint['metadata']['authlevel']
        else:
            authLevel = 'verify-token'
            logger.warning('No authLevel specified for endpoint ' +
                            endpoint['endpointIdentifier'] + ', defaulting to verify-token')

        if authLevel in self.AUTHENTICATION_METHODS:
            return self.AUTHENTICATION_METHODS[authLevel]
        else:
            return self.noAuthenticationMethodIsAvailable


class PlannerPermissionValidator(StandardValidator):
    def __init__(self):
        super().__init__()
        self.PERMISSION_METHODS = {
            'public': lambda: None  # No authentication required
        }

    def generateEvaluationMethod(self, permission):
        def evaluate(plannerId, userId=None):
            authResult = core.auth.plannerPermission(
                permission, userId=userId, plannerId=plannerId)
            if not authResult.succeeded:
                raise ValidationError(authResult.code, authResult.message)

        if permission == 'public':
            return lambda: None
        else:
            return evaluate

    def getEvaluationMethod(self, endpoint, protocolName):
        if 'plannerpermission' in endpoint['metadata']:
            return self.generateEvaluationMethod(endpoint['metadata']['plannerpermission'])
        return lambda: None
