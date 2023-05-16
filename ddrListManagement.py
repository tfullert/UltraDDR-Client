import json
import urllib.parse
from ddrClient import DDRClient
from pprint import pprint

# =============================================================================
# Derived class for managing lists in UDDR.
# =============================================================================
        
class ListManager(DDRClient):

    def __init__(self, apiKey, apiHost=DDRClient.hostOptions['default']):
        DDRClient.__init__(self, apiKey, apiHost)
        
    def getListIds(self, params):
        
        # params (dict):
        #   * datatype (string) = domain, fqdn, registrar, cidr, ip, nameserver, tld
        #   * enabled (string)  = true, false
        #   * type (string)     = allow, deny
        
        rsp = self.doGet('/data/list', {}, params)
        return rsp
    
    def getList(self, listId):
    
        # listId (string) = Id of list to retrieve
        
        rsp = self.doGet('/data/list/' + listId, {}, {})
        return rsp
    
    def createList(self, dryRun, data):
    
        # dryRun (string):          = true, false
        # data (dict):
        #   * datatype (string)     = domain, fqdn, registrar, cidr, ip, nameserver, tld
        #   * enabled (string)      = true, false
        #   * type (string)         = allow, deny
        #   * name (string)         = name of the list
        #   * notes (string)        = notes to apply to the list
        #   * url (string)          = url to download list data from
        #   * interval (string)     = hourly, daily, weekly, monthly
        #   * data (string)         = item to add to list??
        #   * createdBy (string)    = email of user creating list
    
        rsp = self.doPost('/data/list?dryrun=' + dryRun, {}, data)
        
        return rsp.json()['listId']

    def createListFromFile(self, params, files):
    
        # params (dict): 
        #   * datatype (string) = domain, fqdn, registrar, cidr, ip, nameserver, tld
        #   * dryrun (string)   = true, false
        #   * enabled (string)  = true, false
        #   * name (string)     = name of the new list
        #   * notes (string)    = notes for the new list
        #   * type (string)     = allow, deny
        # files (dict):
        #   * file (tuple):     = ("List.txt", open("List.txt", "rb"), "text/plain")
        
        rsp = self.doPostMultiPartFile('/data/list/import', {}, params, files)
        print(rsp.status_code)
        return rsp
        
    def deleteList(self, listId):
        
        # listId (string) = list ID value returned from createList or getLists
        
        rsp = self.doDelete('/data/list/' + listId)
        return rsp
    
    def addItemToList(self, listId, data):
 
        # listId (string)           = ID of list to add to
        # data (dict):
        #   * value (string)        = value to add to the list (ex: www.example.com for domain type list)
        #   * notes (string)        = notes to add to the list item
        #   * enabled (string)      = true, false
        #   * createdBy (string)    = user who created the list item
        
        rsp = self.doPost('/data/list/' + listId, {}, data)
        
        return rsp
        
if __name__ == "__main__":

    apiKey  = '8fd02917-d989-4bb7-b568-14d79c8f58bb' 
    client  = ListManager(apiKey)
    
    # Test display
    print(repr(client))
    print(client)
    
    # Test getting a list of IDs
    listParams = {'datatype': 'fqdn', 'enabled': 'true', 'type': 'deny'}
    rsp = client.getListIds(listParams)
    print("** getListIds RSP:")
    pprint(rsp.json())
    
    # Grab first list to use in later test
    listToUpdate = rsp.json()['local'][0]
    print("LIST NAME:", listToUpdate['name'])
    print("LIST ID:", listToUpdate['id'])
    
    # Test getting a list
    rsp = client.getList(listToUpdate['id'])
    print("** getList RSP:")
    pprint(rsp.json())
    
    # Test updating a list with a new item
    itemToAdd = {'value': 'mynewvalue.com', 'notes': 'added via api', 'enabled': 'true', 'createdBy': 'tfullert'}
    rsp = client.addItemToList(listToUpdate['id'], itemToAdd)
    print("** addItemToList RSP:")
    pprint(rsp.json())
    
    # Test createList
    createListParams = {'datatype': 'domain', 'enabled': 'true', 'type': 'allow', 'name': 'my_test_list', 'notes': 'api_generated', 'data': 'something.com', 'createdBy': 'tfullert'}
    newListId = client.createList('false', createListParams)
    print("** createList RSP:", newListId)
    
    # Test deleteList
    rsp = client.deleteList(newListId)
    print("** deleteList RSP:", rsp.status_code)
    
    # Test createListFromFile
    params = {'datatype': 'domain', 'dryrun': 'false', 'enabled': 'true', 'name': 'newl ist', 'notes': 'from file', 'type': 'deny'}
    #params['clientId'] = 'e41c4cb7-2c17-4257-95a4-f116f9117419'
    files = {
        "file" : ("List.txt", open("List.txt", "rb"), "text/plain")
    }
    rsp = client.createListFromFile(params, files)
    print("RSP:", rsp.text)
    