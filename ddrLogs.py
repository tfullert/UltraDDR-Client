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

if __name__ == "__main__":

    start   = "2023-04-20T01:21:58.283Z"
    end     = "2023-04-24T01:21:58.283Z"
    apiKey  = '[TODO: API KEY HERE]'
    client  = LogManager(apiKey)
    
    rsp = client.getLogs(start, end)

    for log in rsp.json()['logs']:
        print("LOG ENTRY:", log)