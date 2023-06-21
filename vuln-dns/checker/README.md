## Checker

The service checker for [ForcAD](https://github.com/pomo-mondreganto/ForcAD/) platform. 


### Usage

Generate ssh keys. Copy public key for user root to host with service. Change the next global variables in checker.py:
```
USERNAME = "root" 
SERVICE_NAME = "dns"    # Service name in Forcad configuration file
PRIVATE_KEY = "dns_key" # The name of ssh private key
```
Use `pfr` checker_type. Add dependencies from checker/requirements.txt to checkers requirements. 
Need rebuild and rerun ForcAD engine.