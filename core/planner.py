from database import Planner, TimePreference, PlannerPermission
from mongoengine.queryset.visitor import Q
import secrets
import time
import logger

def newPlanner(plannerName, notBefore, notAfter, createdBy):
    plannerId = secrets.token_hex(8)
    planner = Planner(plannerId=plannerId, plannerName=plannerName,
                      notBefore=notBefore, notAfter=notAfter, createdBy=createdBy, creationTime=time.time())
    planner.save()
    logger.debug('Created planner: ' + plannerId)
    return plannerId

def getPlanner(plannerId):
    planner = Planner.objects(plannerId=plannerId).first()
    logger.debug('Retrieved planner: ' + plannerId)
    return planner

def editPlanner(plannerId, properties):
    planner = getPlanner(plannerId)
    protectedProperties = ['createdBy', 'creationTime']
    for property in protectedProperties:
        if property in properties:
            logger.warning('Attempted to edit protected property: ' + property)
            return False

    if planner:
        for key in properties:
            setattr(planner, key, properties[key])
        try:
            planner.save()
            logger.debug('Edited planner: ' + plannerId)
            return True
        except Exception as e:
            logger.error('Failed to edit planner: ' + plannerId + '\n' + str(e))
            return False
    return False

def deletePlanner(plannerId):
    planner = getPlanner(plannerId)
    if planner:
        planner.delete()
        logger.debug('Deleted planner: ' + plannerId)
        return True
    return False

def listUserPlannerIds(userId):
    # planners = Planner.objects.filter(createdBy=userId).values_list('plannerId') # User-created planners
    # for planner in PlannerPermission.objects(userId=userId):
    #     if planner.permission != [] and planner:
    userCreated = Planner.objects(createdBy=userId)
    planners = []
    for planner in userCreated:
        planners.append(planner.plannerId)
    for planner in PlannerPermission.objects(userId=userId):
        # Planners that the user have access to
        if planner.permissions != [] and planner.plannerId not in planners:
            planners.append(planner.plannerId)
    for timePreference in TimePreference.objects(userId=userId):
        # Planners that the user have at least one preference to
        if timePreference.plannerId not in planners:
            planners.append(timePreference.plannerId)
    logger.debug(f'Retrieved planner ids {str(planners)} for user: ' + userId)
    return planners