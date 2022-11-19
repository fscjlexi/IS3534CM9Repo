#!/usr/bin/env python3
#networkFileRW.py
#Lexi Rossow
#Thursday, November 11, 2022
#Update routers and switches;
#read equipment from a file, write updates & errors to file

#file constants 
#Read 
EQUIPR = "equip_r.txt"
EQUIPS = "equip_s.txt"
#Write
OUTPUT_UPDATED = "updated.txt"
OUTPUT_INVALID = "invalid.txt"

##---->>>> Use a try/except clause to import the JSON module
try:
    import json
except ImportError:
    print("An import error has occurred.")


#prompt constants
UPDATE = "\nWhich device would you like to update "
QUIT = "(enter x to quit)? "
NEW_IP = "What is the new IP address (111.111.111.111) "
SORRY = "Sorry, that is not a valid IP address\n"

#function to get valid device
def getValidDevice(routers, switches):
    validDevice = False
    while not validDevice:
        #prompt for device to update
        device = input(UPDATE + QUIT).lower()
        if device in routers.keys():
            return device
        elif device in switches.keys():
            return device
        elif device == 'x':
            return device  
        else:
            print("That device is not in the network inventory.")

#function to get valid IP address
def getValidIP(invalidIPCount, invalidIPAddresses):
    validIP = False
    while not validIP:
        ipAddress = input(NEW_IP)
        octets = ipAddress.split('.')
        #print("octets", octets)
        for byte in octets:
            byte = int(byte)
            if byte < 0 or byte > 255:
                invalidIPCount += 1
                invalidIPAddresses.append(ipAddress)
                print(SORRY)
                break
        else:
            #validIP = True
                return ipAddress, invalidIPCount
                #don't need to return invalidIPAddresses list - it's an object
        
def main():
     
    #dictionaries
    ##---->>>> read the routers and addresses into the router dictionary  
    routers = {}
    with open(EQUIPR, "r") as routerfile: 
        routers = json.load(routerfile)


    ##---->>>> read the switches and addresses into the switches dictionary
    switches = {}
    with open(EQUIPS, "r") as switchfile:
        switches = json.load(switchfile)

    #the updated dictionary holds the device name and new ip address
    updated = {}

    #list of bad addresses entered by the user
    invalidIPAddresses = {}

    #accumulator variables
    devicesUpdatedCount = 0
    invalidIPCount = 0

    #flags and sentinels
    quitNow = False
    validIP = False

    print("Network Equipment Inventory\n")
    print("\tequipment name\tIP address")
    print(routers)
    print(switches)
    
    for router, ipa in routers.items(): 
        print("\t" + router + "\t\t" + ipa)
    for switch, ipa in switches.items():
        print("\t" + switch + "\t\t" + ipa)

    while not quitNow:

        #function call to get valid device
        device = getValidDevice(routers, switches)
        
        if device == 'x':
            quitNow = True
            break
        
        #function call to get valid IP address
        #python lets you return two or more values at one time
        ipAddress, invalidIPCount = getValidIP(invalidIPCount, invalidIPAddresses)
  
        #update device
        if 'r' in device:
            #modify the value associated with the key
            routers[device] = ipAddress 
            print("routers", routers)
        else:
            switches[device] = ipAddress

        devicesUpdatedCount += 1
        #add the device and ipAddress to the dictionary
        updated[device] = ipAddress

        print(device, "was updated; the new IP address is", ipAddress)
        #loop back to the beginning

    #user finished updating devices
    print("\nSummary:")
    print()
    print("Number of devices updated:", devicesUpdatedCount)

    ##---->>>> write the updated equipment dictionary to a file
    OUTPUT_UPDATED.write(updated) 
    
    print("Updated equipment written to file 'updated.txt'")
    print()
    print("\nNumber of invalid addresses attempted:", invalidIPCount)

    ##---->>>> write the list of invalid addresses to a file 
    OUTPUT_INVALID.write(invalidIPAddresses)
    

    print("List of invalid addresses written to file 'errors.txt'")

#top-level scope check
if __name__ == "__main__":
    main()



