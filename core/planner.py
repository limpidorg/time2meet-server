from database import Planner
import secrets


def newPlanner(plannerName, notBefore, notAfter):
    plannerId = secrets.token_hex(8)
    planner = Planner(plannerId=plannerId, plannerName=plannerName,
                      notBefore=notBefore, notAfter=notAfter)
    planner.save()
    return plannerId

def getPlanner(plannerId):
    planner = Planner.objects(plannerId=plannerId).first()
    return planner

def editPlanner(plannerId, properties):
    planner = getPlanner(plannerId)
    if planner:
        for key in properties:
            setattr(planner, key, properties[key])
        planner.save()
        return True
    return False

def deletePlanner(plannerId):
    planner = getPlanner(plannerId)
    if planner:
        planner.delete()
        return True
    return False