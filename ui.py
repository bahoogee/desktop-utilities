
import json
import os
import subprocess

CENTER_SCREEN = 155

def clear_screen():
    
    if os.name == 'nt':
        os.system('cls')

    else:
        os.system('clear')


def title_builder(opt):
    with open('./interface_settings.json') as f:
        ui_settings = json.load(f) 
        
        for m in ui_settings:
            
            if m["id"] == opt:
                title = m["title"]
                if len(title) >= 26:
                    title_length = len(title)  
                elif (len(title) % 2) != 0:
                    title_length = 25
                else: 
                    title_length = 26

                #title_padding = 26 - len(title) if len(title) < 26 else 0
                border = '=' * title_length
                #title = ' ' * (int(title_padding/2)) + title + ' ' * (int(title_padding/2))
                
                # print program title
                print("\n\n\n")                         # top margin
                print(border.center(CENTER_SCREEN))     # top title border
                print(title.center(CENTER_SCREEN))      # title
                print(border.center(CENTER_SCREEN))     # bottom title border
                print("\n\n\n")                         # title margin

def menu_builder(opt):
    longest_row = 0
    with open('./interface_settings.json') as f:
        ui_settings = json.load(f) 
        for m in ui_settings:
            if m["id"] == opt:  
                # get length of longest record
                for o in m["options"]:
                    menu_opt = "[" + o["opt"] + "]  " + o["desc"]
                    if len(menu_opt) > longest_row:
                        longest_row = len(menu_opt)  
                
                # print menu
                for o in m["options"]:
                    menu_opt = "[" + o["opt"] + "]  " + o["desc"]
                    menu_item = menu_opt.ljust(longest_row)
                    menu_rec = menu_item.center(CENTER_SCREEN)
                    print(menu_rec)
                
                

def interface_builder(opt, menu_title):
    clear_screen()
    title_builder(opt)
    print(menu_title.center(CENTER_SCREEN))
    print()
    menu_builder(opt)
    print("\n"*2)

def help_screen(screen):
    import sys
    clear_screen()
    # set vars
    start_printing = False
    longest_line = 0
    help_file_content = ""

    with open('./help.md', 'r') as help_file:
        # determine the longest line - for formatting help page
        for line in help_file:
            if line.strip() == '[' + screen + ']':
                start_printing = True
            elif start_printing:
                if line[0] == '[':
                    break        
                if len(line) > longest_line:
                    longest_line = len(line)
 
    start_printing = False      # reset printing var
    print("\n\n\n")
    with open('./help.md', 'r') as help_file:
        # read file and print related lines for help screen
        for line in help_file:
            if line.strip() == '[' + screen + ']':
                start_printing = True
            elif start_printing:
                if line[0] == '[':
                    return
                help_file_content = line.ljust(longest_line)
                output_line = help_file_content.center(CENTER_SCREEN)
                print(output_line.rstrip())



def prng():

    import random

    # initialize vars
    upper_limit = 1000000000        # rand num upper limit = 1B

    return random.randint(0, upper_limit)


def restaurant_picker():
    with open('./restaurants.json') as f:
            restaurants = json.load(f) 
    
    # gen random # then select restaurant associated with the gen number
    num = prng()
    total_restaurants = len(restaurants)
    selection = num if num <= total_restaurants else num % total_restaurants

    pick = restaurants[selection]
    value = "Recommended Restaurant: " + pick

    clear_screen()
    # build interface to report to user
    # title
    title_builder("R")
    print("\n"*1)

    # results
    print(value.center(CENTER_SCREEN))
    print("\n"*4)

    # options menu
    menu_title = "Options"
    print(menu_title.center(CENTER_SCREEN))
    print("\n"*2)
    menu_builder("R")
    print("\n"*2)

def winddir(degree):
    if degree == 0:
        return ""
    
    value = int(degree / 22.5)
    match value:
        case 0: dir = 'N'
        case 1: dir = 'NNE'
        case 2: dir = 'NE'
        case 3: dir = 'ENE'
        case 4: dir = 'E'
        case 5: dir = 'ESE'
        case 6: dir = 'SE'
        case 7: dir = 'SSE'
        case 8: dir = 'S'
        case 9: dir = 'SSW'
        case 10: dir = 'SW'
        case 11: dir = 'WSW'
        case 12: dir = 'W'
        case 13: dir = 'WNW'
        case 14: dir = 'NW'
        case 15: dir = 'NNW'
        case 16: dir = 'N'
        case _: dir = ""
    
    return dir


def current_weather_reporter(weather_json, zipcode):
    longest_rec = 0
    clear_screen()
    # build interface to report to user
    # title
    title_builder("C")
    print("\n"*1)

    # extract weather data
    try:
        # format and display results to user
        curr_weather = json.loads(weather_json)
        title = "Current Weather for: " + zipcode
        cond = curr_weather["weather"][0]["description"]
        temp = round(curr_weather["main"]["temp"])
        feel_like = round(curr_weather["main"]["feels_like"])
        wind = round(curr_weather["wind"]["speed"])
        cond_txt =      "Condition:   " + cond
        temp_txt =      "Temperature: " + str(temp) + "F"
        feel_like_txt = "Feels Like:  " + str(feel_like) + "F"
        wind_txt =      "Wind:        " + str(wind) + " mph " + str(winddir(curr_weather["wind"]["deg"]))

        longest_rec = len(cond_txt) if len(cond_txt) >= len(wind_txt) else len(wind_txt)
        longest_rec = longest_rec if longest_rec >= len(temp_txt) else len(temp_txt)
        longest_rec = longest_rec if longest_rec >= len(feel_like_txt) else len(feel_like_txt)

        row1 = cond_txt.ljust(longest_rec)
        row2 = temp_txt.ljust(longest_rec)
        row3 = feel_like_txt.ljust(longest_rec)
        row4 = wind_txt.ljust(longest_rec)

        # results
        print(title.center(CENTER_SCREEN))
        print('\n'*2)
        print(row1.center(CENTER_SCREEN))
        print(row2.center(CENTER_SCREEN))
        print(row3.center(CENTER_SCREEN))
        print(row4.center(CENTER_SCREEN))
        print("\n"*4)

    except:
        # results
        print()
        print(weather_json.center(CENTER_SCREEN))
        print()
        print()
        print("\n"*4)

    # options menu
    menu_title = "Options"
    print(menu_title.center(CENTER_SCREEN))
    print("\n"*2)
    menu_builder("C")
    print("\n"*2)


def weather():
    import zmq 
    interface_builder("W", "Options")

    print("\n\n")
    while True:
        menu_option = input("Enter Option > ")
        menu_option = menu_option.strip().capitalize()
        match menu_option:
            case "C":
                user_input = ''

                # setup client
                context = zmq.Context()

                # setup socket
                socket = context.socket(zmq.REQ)

                # connect to service socket
                socket.connect("tcp://localhost:5555")

                # start up weather service
                #subprocess.run(['python3', './weather_service.py'], start_new_session=True)
                os.system('python3 ./weather_service.py &')
                
                while True:
                    if user_input == 'C' or user_input == '':
                        # get the zip code
                        zip_code = input("\nEnter zip code > ")

                        # send message to service 
                        socket.send_string(zip_code.strip())

                        # receive reply and display to user
                        message = socket.recv()
                        current_weather_reporter(message.decode(), zip_code.strip()) 
                        
                        # get user input
                        user_input = input("Enter option > ")
                        user_input = user_input.strip().capitalize()
                        
                    # check if re-run or exit
                    if user_input == "W":       # exit to Weather menu
                        # send shutdown message to service 
                        socket.send_string('shutdown')
                        interface_builder("W", "Options")
                        break
                    elif user_input != 'C':
                        print("Invalid option!")
                        # get user input
                        user_input = input("\nEnter option > ")
                        user_input = user_input.strip().capitalize()

            case "H":
                help_screen("WEATHER")
                while True:
                    print()
                    user_input = input("Enter X to exit help > ")
                    if user_input.strip().capitalize() == 'X':
                        interface_builder("W", "Options")
                        break
                    else:
                        print("Invalid option!")
            case "M":
                interface_builder("M", "Main Menu")
                return
            case _:
                print("\nUnknown option!\n\n")


def prog():
 
    interface_builder("M", "Main Menu")
    
    while True:
        menu_option = input("Enter Option > ")
        menu_option = menu_option.strip().capitalize()
        match menu_option:
            case "E":
                print("\n"*2)
                return
            case "M":
                interface_builder("M", "Main Menu")
            case "R":
                restaurant_picker()
                    
                while True:
                    # get user input
                    user_input = input("Enter option > ")
                    user_input = user_input.strip().capitalize()
                    match user_input:
                        case "R":
                            print("\nCONFIRMATION: Re-running the Restaurant Recommender will cause the current recommendation to be lost!\n\n")
                            user_input = input("Do you wish to proceed [Y or N] > ")
                            if user_input.strip().capitalize() == "Y":
                                restaurant_picker()

                        case "M":
                            interface_builder("M", "Main Menu") 
                            break
                        case _:
                            print("\nUnknown option!\n\n")

            case "W":
                weather()

            case "H":
                help_screen("PROGRAM")
                while True:
                    user_input = input("Enter X to exit help > ")
                    if user_input.strip().capitalize() == 'X':
                        interface_builder("M", "Menu Options")
                        break
                    else:
                        print("Invalid option!")




if __name__ == "__main__":
    prog()

