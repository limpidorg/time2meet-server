from RequestMap.Validators.ValidatorBase import StandardValidator, ValidationError

class AuthenticationValidator(StandardValidator):
    def __init__(self, request_map):
        super().__init__(request_map)
        AUTHENTICATION = {
            'verify-token': self.verifyToken,
        }
    
    def verifyToken(username, token):
        pass

    def getEvaluationMethod(self, endpoint):
        if 'authLevel' in endpoint['metadata']:
            authLevel = endpoint['metadata']['authLevel']
        else:
            authLevel = 'verify-token'
        
        return self.evaluateAuthentication