# UltraDDR-Client

UltraDNS Detection and Response (UDDR) is the next generation of protective DNS, a solution that goes into action before an attack, rather than after. Effectively countering adversaries and blocking malicious 
queries proactively, giving you the ability to get ahead of threats and attacks.  UltraDDR concentrates on the discovery and mapping of adversary infrastructure combined with real-time communication pattern analysis 
to shift your security defenses from reactive to proactive.  The UltraDDR-Client code project provides Client API code for accessing the [UltraDDR API](https://api.ddr.ultradns.com/docs/ultraddr/).

## Files

This project consists of the following files:

* ddrClient.py - This is the base UltraDDR client code that is used by other classes.
* ddrListManagement.py - Client code used for creating, updating, and deleting block/allow lists on UltraDDR.
* ddrLogs.py - Client code used for retrieving raw log data from UltraDDR. 

## Requirements

You will need the following in order to use this project:

* [UltraDDR API key](https://ddr.ultradns.com/static/login)
* [Python 3](https://www.python.org/downloads/)
* [requests library](https://requests.readthedocs.io/en/latest/)

## Usage

Once the project is downloaded, files extracted, and UltraDDR API key procured you can use the code as follows:

### List Management

Import the library and create a ListManager client:

```python
from ddrListManagement import ListManager

apiKey  = '00000000-0000-0000-0000-000000000000'
client  = ListManager(apiKey)
```

Sample code to get a list of lists from an UltraDDR account:

```python
plist   = {'datatype': 'fqdn', 'enabled': 'true', 'type': 'deny'}
rsp     = client.getListIds(plist)
```

Or you can create a new list with entries from a file on disk:

```python
params  = {'datatype': 'domain', 'dryrun': 'false', 'enabled': 'true', 'name': 'newl list', 'notes': 'created from file', 'type': 'deny'}
files   = {"file" : ("List.txt", open("List.txt", "rb"), "text/plain")}
rsp     = client.createListFromFile(params, files)
```
