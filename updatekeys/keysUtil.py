'''
Created on Nov 3, 2015

@author: Zhou
'''
import hashlib,constants
from incident.models import Incident
from agency.models import Agency
from updatekeys.models import updatesKeys


def generateKey(incidentID , agencyID):
    
    # if existing key. ignore 
    query = updatesKeys.objects.all().filter(incidentID = incidentID, agencyID = agencyID)
    if query:
        return constants.BASEURL + query[0].keys 
    
    keyObject = hashlib.md5()
    keyObject.update(incidentID.__str__() + '&' + agencyID.__str__())
    for _ in range(constants.ENCRYPT_LEVEL):
        key = keyObject.hexdigest()
        keyObject = hashlib.md5()
        keyObject.update(key)
    key = keyObject.hexdigest()
    keyInstance = updatesKeys(incidentID = Incident.objects.get(pk = incidentID), agencyID = Agency.objects.get(pk = agencyID), keys = key)
    keyInstance.save()
    return constants.BASEURL + keyInstance.keys

'''
key = keys in data
return {incidentID,agencyID}
'''
def verifyKey(key):
    queryset = updatesKeys.objects.all().filter(keys = key)
    if not queryset:
        return ()
    if queryset[0].incidentID.status == "closed":
        return ()
    return {"incidentID" : queryset[0].incidentID.id , "agencyID" : queryset[0].agencyID.id}   