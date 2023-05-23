import json
import urllib.parse
from ddrClient import DDRClient
from pprint import pprint

class LogManager(DDRClient):

    def __init__(self, apiKey, apiHost=DDRClient.hostOptions['alternate']):
        DDRClient.__init__(self, apiKey, apiHost)
    
    def getLogs(self, startDateTime, endDateTime):
    
        # Construct data for query
        data = {
            "applied_filters": [{
                "exclude": False,
                "id": "datetime",
                "isRange": True,
                "rangeValue": {
                    "end": endDateTime,
                    "start": startDateTime
                }
            }]
        }
        
        rsp = client.doPost('/api/protect/ext/logs', {}, data)
        return rsp
    
    def getLogsV2(self, startDateTime, endDateTime):
    
        # Save host configuration since we have to change it for this call
        backupHost      = self.apiHost
        self.apiHost    = DDRClient.defaultHost
        
        data = {
            "applied_filters": [{
                "exclude": False,
                "id": "datetime",
                "isRange": True,
                #"partial": False,
                "rangeValue": {
                    "end": endDateTime,
                    "start": startDateTime
                }
            }],
            "paging": {
                "order": "desc",
                "sort": "datetime",
                "page_number": 0,
                "page_size": 10000,
                "page_type": "standard"
            }
        }
        
        rsp = client.doPost('/dns-log-report/v2/logs', {}, data)
        
        # Return host to what it was prior to the callable
        self.apiHost = backupHost
        
        return rsp

if __name__ == "__main__":

    start   = "2023-04-20T01:21:58.283Z"
    end     = "2023-04-24T01:21:58.283Z"
    apiKey  = '[TODO: API KEY HERE]'
    client  = LogManager(apiKey)
    
    rsp = client.getLogsV2(start, end)
    print("RSP:", rsp.text)
    
    #rsp = client.getLogs(start, end)

    #for log in rsp.json()['logs']:
    #    print("LOG ENTRY:", log)
        
        