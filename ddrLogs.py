import json
import urllib.parse
from ddrClient import DDRClient
from pprint import pprint

def getLogs():

    apiKey  = '[TODO: API KEY HERE]'
    client  = DDRClient(apiKey, DDRClient.hostOptions['alternate'])

    data    = {
                "applied_filters":  [
                    {
                        "exclude": False,
                        "id": "datetime",
                        "isRange": True,
                        "rangeValue": {
                            "end": "2023-04-24T01:21:58.283Z",
                            "start": "2023-04-20T01:21:58.283Z"
                        }
                    }
                ]
             }

    rsp = client.doPost('/api/protect/ext/logs', {}, data)
    print("URL:", rsp.url)
    
    pprint(rsp.json())
    
getLogs()
