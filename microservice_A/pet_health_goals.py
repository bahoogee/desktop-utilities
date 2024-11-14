


import json
import zmq


def list_goals():
    # Purpose: Returns the pet health goals list
    with open('./pet_health_goals.json') as file:
        pet_goals_file = json.load(file)

    return pet_goals_file

def add_goal(new_pet_goal):
    # Purpose: adds a new pet health goal then resequences the list
    
    try:
        new_record = {"goal_num": 0, "pet_name": new_pet_goal[0], "pet_goal": new_pet_goal[1], "goal_date": new_pet_goal[2]}
        
        # load the pet health goals file
        with open('./pet_health_goals.json', 'r') as file:
            pet_goals_file = json.load(file) 
            
        # add new pet health goal
        pet_goals_file.append(new_record)
        
        # sort and resequence the list of goals - by goal date
        num = 1
        sorted_goals = sorted(pet_goals_file, key=lambda x: x["goal_date"])
        
        for rec in sorted_goals:
            rec['goal_num'] = num
            num += 1

        # convert back to json
        with open('./pet_health_goals.json', 'w') as file:
            json.dump(sorted_goals, file, indent=4)
            return 0
    except:
        return 1


def delete_goal(goal_num):
    # Purpose: deletes a pet health goal then resequences the list
    try:
        # load the pet health goals file
        with open('./pet_health_goals.json', 'r+') as file:
            pet_goals_file = json.load(file) 

        # deletes pet health goal
        updated_file = [x for x in pet_goals_file if int(x.get("goal_num")) != int(goal_num)]

        # sort and resequence the list of goals - by goal date
        num = 1
        sorted_goals = sorted(updated_file, key=lambda x: x["goal_date"])

        for rec in sorted_goals:
            rec['goal_num'] = num
            num += 1

        # convert back to json
        with open('./pet_health_goals.json', 'w') as file:
            json.dump(sorted_goals, file, indent=4)
            return 0
    except:
        return 1
    
def prog():
    # initialize service
    context = zmq.Context()
    
    # setup service socket
    socket = context.socket(zmq.REP)
    try:
        socket.bind("tcp://*:5555")
    except:
        print("error")
        return 1
    
    # setup service to listen
    while True:
        # monitor comm socket for client message
        message = socket.recv()
        
        # check if message received and if message is to quit
        if len(message) > 0:
            
            if message.decode() == 'shutdown': # Client asked service to quit
                break

            # process incoming message from client
            req = json.loads(message.decode())

            # determine function requested to be run
            if req["function"].upper() == "LIST":
                socket.send_json(list_goals())
                
            elif req["function"].upper() == "ADD":
                if add_goal(req["Opt"]) == 0:
                    socket.send_string("ok")
                else:
                    print("Prog: Error")
                    socket.send_string("error")
            elif req["function"].upper() == "DELETE":
                if delete_goal(req["Opt"]) == 0:
                    socket.send_string("ok")
                else:
                    socket.send_string("error")
            else:
                socket.send_string("error")


    # termination service socket
    context.destroy()
    
if __name__ == '__main__':
    prog()
