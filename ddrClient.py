import json
import requests

# =============================================================================
# Base class to implement UltraDDR API Client.
# =============================================================================

class DDRClient:
    
    hostOptions = {
        'default'   : "https://api.ddr.ultradns.com",
        'alternate' : "https://ddr.ultradns.com"
    }
    
    defaultHost = hostOptions['default']
    
    baseHeaders = {
        "Content-Type"  : "application/json",
        "Accept"        : "application/json"
    }
    
    def __init__(self, apiKey, apiHost=defaultHost):
        self._apiHost = apiHost
        self._apiKey = apiKey

    def __str__(self):
        return self._apiKey
    
    def __repr__(self):
        return f'DDRClient("{self.apiKey}", "{self.apiHost}")'
    
    @property
    def apiHost(self):
        return self._apiHost
        
    @property
    def apiKey(self):
        return self._apiKey
    
    @apiHost.setter
    def apiHost(self, apiHost=defaultHost):
        self._apiHost = apiHost
        
    @apiKey.setter
    def apiKey(self, apiKey):
        self._apiKey = apiKey

    def getURL(self, path):
        return self.apiHost + path
    
    def prepHeaders(self, headers=None):
        if headers is None:
            headers = {}
            
        return {"X-API-Key": self.apiKey} | DDRClient.baseHeaders | headers
        
    def doGet(self, path='', headers=baseHeaders, params=None):
        
        rsp = requests.get(self.getURL(path), headers=self.prepHeaders(headers), params=params)
        return rsp
    
    def doPost(self, path='', headers=baseHeaders, data=None):

        rsp = requests.post(self.getURL(path), headers=self.prepHeaders(headers), data=json.dumps(data))  
        return rsp
        
    def doPostMultiPartFile(self, path='', headers=baseHeaders, params=None, files=None):
    
        rsp = requests.post(self.getURL(path), headers=self.prepHeaders(headers), params=params, files=files) 
        return rsp
               
    def doPut(self, path='', headers=baseHeaders, params=None):
    
        rsp = requests.put(self.getURL(path), headers=self.prepHeaders(headers), json=params)
        return rsp
    
    def doDelete(self, path='', headers=baseHeaders):
    
        rsp = requests.delete(self.getURL(path), headers=self.prepHeaders(headers)) 
        return rsp
            
# =============================================================================
# Test functionality of list API calls.
# =============================================================================
if __name__ == "__main__":
    
    apiKey  = '[TODO: API_KEY_HERE]'
    client  = DDRClient(apiKey)
    
    # Test client display and getters
    print("REPR:", repr(client))
    print("CLIENT:", client)
    print("HOST:", client.apiHost)
    print("KEY:", client.apiKey)
    
    # Test helpers
    print("URL:", client.getURL("/simple/test/path"))
    
    # Test header modification
    print("HEADERS (BASE):", DDRClient.baseHeaders)
    print("HEADERS MOD (EXTRA):", client.prepHeaders({'Accept': 'application/pdf'}))
    print("HEADERS MOD (NONE):", client.prepHeaders())
    
    # Test HTTP verbs
    
    # Test doGet
    rsp = client.doGet('/data/list', params={'datatype': 'fqdn', 'type': 'deny'})
    print("RSP (GET):", rsp.text)
    
    # Test doPost
    client.apiHost = DDRClient.hostOptions['alternate']
    data = {"applied_filters": {"query_type": "domain", "top_count": '25'}}
    rsp = client.doPost('/api/protect/ext/aggregates', {}, data)
    print("RSP (POST):", rsp.text)
    
    # TODO: Test doPostMultiPartFile
    # TODO: Test doPut
    # TODO: Test doDelete
    
    # Test client setters
    client.apiHost = DDRClient.defaultHost
    print("HOST:", client.apiHost)
    
    client.apiKey = "00000000-0000-0000-0000-000000000000"
    print("KEY:", client.apiKey)

# =============================================================================