def desensitizeUser(userDict: dict) -> dict:
    protectedProperties = ['password', 'salt', 'tokens']
    # Remove useless _id
    del userDict['_id']
    # Desensitize the user object
    for protectedProperty in protectedProperties:
        if protectedProperty in userDict:
            del userDict[protectedProperty]
    return userDict

def desensitizePlanner(plannerDict: dict) -> dict:
    protectedProperties = []
    # Remove useless _id
    del plannerDict['_id']
    # Desensitize the planner object
    for protectedProperty in protectedProperties:
        if protectedProperty in plannerDict:
            del plannerDict[protectedProperty]
    return plannerDict