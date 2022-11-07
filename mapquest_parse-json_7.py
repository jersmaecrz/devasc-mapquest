import json
import urllib.parse
import requests
from datetime import datetime, timedelta #Time Module

main_api = "https://www.mapquestapi.com/directions/v2/route?"
alt_api = "https://www.mapquestapi.com/directions/v2/alternateroutes?"
opt_api = "https://www.mapquestapi.com/directions/v2/optimizedroute?"
key = "FOTlw2yQDHUrzjGqNZ7sHcHtu1eUXmb5"

def  computeETA(time):
    duration = float((time)/60) #duration seconds converted to minutes
    startTime = (datetime.now().strftime("%I:%M %p"))
    estimatedTimeOfArrival = str(((datetime.now() + timedelta(minutes=duration)).strftime("%I:%M %p")))
    print("Start Time: " + startTime)
    print("Estimated Time of Arrival: " + estimatedTimeOfArrival)
    print("Realtime Trip Duration: " + str("{:.2f}".format(duration)) + " min")

while True:
    
    # take user inputs
    orig = input("Starting Location: ")
    if orig == "quit" or orig == "q":
        break
    print()
    loc = input("Stopover: ")
    if loc == "quit" or loc == "q":
        break
    print()
    dest = input("Destination: ")
    if dest == "quit" or dest == "q":
        break
    print("\n")

    # append entries for the Optimized Route
    locs = "{\"locations\":[\"" + orig + "\",\"" + loc + "\",\"" + dest + "\"]}"

    # make url
    url = main_api + urllib.parse.urlencode({"key":key, "from":orig, "to":dest})
    url_alt = alt_api + urllib.parse.urlencode({"key":key, "from":orig, "to":dest})
    url_opt = opt_api + urllib.parse.urlencode({"json":locs, "key":key})

    print("URL: " + url)
    print("URL ALT: " + url_alt)
    print("URL OPT: " + url_opt)
    
    # request json files
    json_data = requests.get(url).json()
    json_data_alt = requests.get(url_alt).json()
    json_data_opt = requests.get(url_opt).json()

    # route
    json_status = json_data["info"]["statuscode"]

    if json_status == 0:
        print("API Status: " + str(json_status) + " = A successful route call.\n")
        print("==============================================")
        print()
        print("Direct directions from " + (orig) + " to " + (dest))
        print("Trip Duration: " + (json_data["route"]["formattedTime"]))
        print("Kilometers: " + str("{:.2f}".format((json_data["route"]["distance"]) * 1.61)))
        # print("Fuel Used (Ltr): " + str("{:.2f}".format((json_data["route"]["fuelUsed"]) * 3.78)))
        computeETA(json_data["route"]["realTime"]) #Display Start Time & ETA (uses real time - w/consideration of traffic)
        print()
        print("==============================================")
        print()
        y = 0
        for each in json_data["route"]["legs"][0]["maneuvers"]:
            y +=1
            print(str(y) + ". " + (each["narrative"]) + " (" + str("{:.2f}".format((each["distance"]) * 1.61) + " km)"))
        print()
        print("==============================================\n")
    elif json_status == 402:
        print("**********************************************")
        print("Status Code: " + str(json_status) + "; Invalid user inputs for one or both locations.")
        print("**********************************************\n")
    elif json_status == 611:
        print("**********************************************")
        print("Status Code: " + str(json_status) + "; Missing an entry for one or both locations.")
        print("**********************************************\n")
    else:
        print("**************************************************************")
        print("For Status Code: " + str(json_status) + "; Refer to:")
        print("https://developer.mapquest.com/documentation/directions-api/status-codes")
        print("**************************************************************\n")

    # alternative route
    json_status_alt = json_data_alt["info"]["statuscode"]

    if json_status_alt == 0:
        print("API Status: " + str(json_status_alt) + " = A successful alternative route call.\n")
        print("==============================================")
        print()
        print("Direct directions from " + (orig) + " to " + (dest))
        print("Trip Duration: " + (json_data_alt["route"]["formattedTime"]))
        print("Kilometers: " + str("{:.2f}".format((json_data_alt["route"]["distance"]) * 1.61)))
        # print("Fuel Used (Ltr): " + str("{:.2f}".format((json_data_alt["route"]["fuelUsed"]) * 3.78)))
        computeETA(json_data_alt["route"]["realTime"]) #Display Start Time & ETA (uses real time - w/consideration of traffic)
        print()
        print("==============================================")
        print()
        y = 0
        for each in json_data_alt["route"]["legs"][0]["maneuvers"]:
            y +=1
            print(str(y) + ". " + (each["narrative"]) + " (" + str("{:.2f}".format((each["distance"]) * 1.61) + " km)"))
        print()
        print("==============================================\n")
    elif json_status_alt == 402:
        print("**********************************************")
        print("Status Code: " + str(json_status_alt) + "; Invalid user inputs for one or both locations.")
        print("**********************************************\n")
    elif json_status_alt == 611:
        print("**********************************************")
        print("Status Code: " + str(json_status_alt) + "; Missing an entry for one or both locations.")
        print("**********************************************\n")
    else:
        print("**************************************************************")
        print("For Status Code: " + str(json_status_alt) + "; Refer to:")
        print("https://developer.mapquest.com/documentation/directions-api/status-codes")
        print("**************************************************************\n") 

    # optimized route
    json_status_opt = json_data_opt["info"]["statuscode"]

    if json_status_opt == 0:
        print("API Status: " + str(json_status_opt) + " = A successful optimized route call.\n")
        print("==============================================")
        print()
        print("Directions from " + (orig) + " to " + (dest) + " with stopovers to " + (loc))
        print("Trip Duration: " + (json_data_opt["route"]["formattedTime"]))
        print("Kilometers: " + str("{:.2f}".format((json_data_opt["route"]["distance"]) * 1.61)))
        # print("Fuel Used (Ltr): " + str("{:.2f}".format((json_data_opt["route"]["fuelUsed"]) * 3.78)))
        computeETA(json_data_opt["route"]["realTime"])
        
        i = 0
        y = 0
        print()
        print("==============================================")
        print()
        while (i < 2):
            for each in json_data_opt["route"]["legs"][i]["maneuvers"]:
                y +=1
                print(str(y) + ". " + (each["narrative"]) + " (" + str("{:.2f}".format((each["distance"]) * 1.61) + " km)"))
            i += 1
            if i == 3:
                print()
                print("==============================================\n")
                print()
            else:
                print()
                print("==============================================")
                print()
        
    elif json_status_opt == 402:
        print("**********************************************")
        print()
        print("Status Code: " + str(json_status_opt) + "; Invalid user inputs for one or both locations.")
        print()
        print("**********************************************\n")
    elif json_status_opt == 611:
        print("**********************************************")
        print()
        print("Status Code: " + str(json_status_opt) + "; Missing an entry for one or both locations.")
        print()
        print("**********************************************\n")
    else:
        print("**************************************************************")
        print()
        print("For Status Code: " + str(json_status_opt) + "; Refer to:")
        print("https://developer.mapquest.com/documentation/directions-api/status-codes")
        print()
        print("**************************************************************\n")