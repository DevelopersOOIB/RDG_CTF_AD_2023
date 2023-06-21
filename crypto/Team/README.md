**To run correctly:**


In the file service.py change the destination port of request_trusted_center to port 1000X,
where **"X"** is your team's subnet number. 


**For example:** 
    Your address: 10.20.1.0; 
    Port: 10001; 

    Your address: 10.20.5.0; 
    Port: 10005; 
    
    And so on... 


**Attention!** 
The use of ports belonging to other teams will lead to a violation of the logic of the service, 
as a result of which the health check system will inform you 
about the incorrect operation of the service, which will affect the points you earn.

**And also specify your ip address.**