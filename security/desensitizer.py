def desensitizeUser(userDict: dict, desensitizeFor: str = 'user') -> dict:

    protectedPropertiesLists = {
        'user': ['password', 'salt', 'tokens', 'email'],
        'owner': ['password', 'salt', 'tokens'],
    }
    protectedProperties = protectedPropertiesLists.get(
        desensitizeFor, ['password', 'salt', 'tokens', 'email'])

    # Remove useless _id
    del userDict['_id']
    # Desensitize the user object
    for protectedProperty in protectedProperties:
        if protectedProperty in userDict:
            del userDict[protectedProperty]
    return userDict


def desensitizePlanner(plannerDict: dict, desensitizeFor: str = 'user') -> dict:
    protectedPropertiesLists = {
        'user': []
    }
    protectedProperties = protectedPropertiesLists.get(desensitizeFor, [])
    # Remove useless _id
    del plannerDict['_id']
    # Desensitize the planner object
    for protectedProperty in protectedProperties:
        if protectedProperty in plannerDict:
            del plannerDict[protectedProperty]
    return plannerDict
