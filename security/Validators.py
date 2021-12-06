from RequestMap.Validators.ValidatorBase import StandardValidator, ValidationError
import core.auth
import logging


class AuthenticationValidator(StandardValidator):
    def __init__(self):
        super().__init__()
        self.AUTHENTICATION_METHODS = {
            'verify-token': self.verifyToken,
            'verify-password': self.verifyPassword,
            'public': lambda: None  # No authentication required
        }

    def verifyToken(self, userId, token):
        if not core.auth.verifyToken(userId, token):
            raise ValidationError(-101)

    def verifyPassword(self, userId, password):
        if not core.auth.verifyPassword(userId, password):
            raise ValidationError(-103)

    def noAuthenticationMethodIsAvailable(self):
        raise ValidationError(-100)  # No authentication method is available

    def getEvaluationMethod(self, endpoint):
        if 'authlevel' in endpoint['metadata']:
            authLevel = endpoint['metadata']['authlevel']
        else:
            authLevel = 'verify-token'
            logging.warning('No authLevel specified for endpoint ' +
                            endpoint['endpointIdentifier'] + ', defaulting to verify-token')

        if authLevel in self.AUTHENTICATION_METHODS:
            return self.AUTHENTICATION_METHODS[authLevel]
        else:
            return self.noAuthenticationMethodIsAvailable
