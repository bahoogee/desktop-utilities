from urllib.request import urlopen
import json
import zmq
import sys

def zip_validator(zipcode):
    if zipcode.strip().isnumeric():
        if int(zipcode) >= 1 and int(zipcode) <=99999:
            return True
    
    return False

def get_current_weather(zipcode):
    # lookup the zip code to get the long, lat for the api string
    api_string = f"https://api.openweathermap.org/data/2.5/weather?zip={zipcode},us&units=Imperial&appid=efbec67ea3f3a4e1f28e02f04dc6c2e9"
    response = urlopen(api_string)
    # receive the weather data
    return json.loads(response.read())


if __name__ == '__main__':
    # initialize service
    context = zmq.Context()

    # setup service socket
    socket = context.socket(zmq.REP)
    try:
        socket.bind("tcp://*:5555")
    except:
        pass

    # setup service to listen
    while True:
        # monitor comm socket for client message
        message = socket.recv()

        # check if message received and if message is to quit
        if len(message) > 0:
            
            if message.decode() == 'shutdown': # Client asked service to quit
                break

            # send back confirmation message of message received by service to client
            if zip_validator(message.decode()):
                message = get_current_weather(message.decode())
                socket.send_json(message)
            else:
                socket.send_string('ERROR: Invalid zip code!')

    # termination service socket
    print("\nTerminating service\n")
    context.destroy()