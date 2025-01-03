# Pet Health Goals microservice

Author: Joshua Moore
Class:  CS 361
Desc:   Microservice that manages a list of pet health goals that is held in an external json file.

## COMMUNICATION CONTRACT:

The Pet Health Goals microservice uses the ZeroMQ message broker to facilitate communication between the microservice and calling program.  This microservice also relies on a json called pet_health_goals.json with a unnamed list within to be available in the common directory.

## Request Data:
To request data from the microservice, send a json containing the name of the function to be run as well as the required argument (if required).

request format: {"function": '[function name]', "Opt": [required argument]}

Functions available:

### LIST: 
- Desc:      provide user with the current list of pet health goals
- Argument:  none
- Example:   {"function": "LIST"}
- Ex. Call:  socket.send_json({"function": "LIST"})

### ADD: 
- Desc:      add a new pet health goal to the list of pet health goals
- Argument:  a python list containing the pet's name, text for the goal, & and the due date for the goal (in YYYY-MM-DD format)
- Example:   {"function": "ADD", "Opt": ["Fluffy", "Lost 10 lbs", "2024-12-05"]}
- Ex. Call:  socket.send_json({"function": "ADD", "Opt": ["Fluffy", "Lost 10 lbs", "2024-12-05"]})

### DELETE: 
- Desc:      delete an existing pet health goal from the list of pet health goals
- Argument:  goal number corresponding to the goal to be deleted
- Example:   {"function": "ADD", "Opt": "2"}
- Ex. Call:  socket.send_json({"function": "ADD", "Opt": "2"})


## Receive Data:
To receive data from the microservice, it depends on the function being used.

Receiving from:

### LIST: 
- Desc:      provide user with the current list of pet health goals
- Data Type: json
- Example:   message = socket.recv()

### ADD: 
- Desc:      add a new pet health goal to the list of pet health goals
- Data Type: string
- Example:   message = socket.recv_string()

### DELETE: 
- Desc:      delete an existing pet health goal from the list of pet health goals
- Data Type: string
- Example:   message = socket.recv_string()

UML Sequence Diagram:

![Microservice UML](https://github.com/user-attachments/assets/f41a2371-7b63-4646-8fe0-ef06cd10a529)
