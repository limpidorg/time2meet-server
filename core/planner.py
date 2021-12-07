from database import Planner
import secrets
import time

def newPlanner(plannerName, notBefore, notAfter, createdBy):
    plannerId = secrets.token_hex(8)
    planner = Planner(plannerId=plannerId, plannerName=plannerName,
                      notBefore=notBefore, notAfter=notAfter, createdBy=createdBy, creationTime=time.time())
    planner.save()
    return plannerId

def getPlanner(plannerId):
    planner = Planner.objects(plannerId=plannerId).first()
    return planner

def editPlanner(plannerId, properties):
    planner = getPlanner(plannerId)
    protectedProperties = ['createdBy', 'creationTime']
    for property in protectedProperties:
        if property in properties:
            return False

    if planner:
        for key in properties:
            setattr(planner, key, properties[key])
        try:
            planner.save()
            return True
        except:
            return False
    return False

def deletePlanner(plannerId):
    planner = getPlanner(plannerId)
    if planner:
        planner.delete()
        return True
    return False