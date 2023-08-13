#!/usr/bin/env python3
# networkFileRW.py
# Chevy Nain
# August 8, 2022
# Update routers and switches;
# read equipment from a file, write updates & errors to file
##---->>>> Use a try/except clause to import the JSON module
##---->>>> Create file constants for the file names; file constants can be reused
## There are 2 files to read this program: equip_r.txt and equip_s.txt
## There are 2 files to write in this program: updated.txt and errors.txt

import json

EQUIP_R_FILE = "equip_r.txt"
EQUIP_S_FILE = "equip_s.txt"
UPDATED_FILE = "updated.txt"
INVALID_FILE = "invalid.txt"

# Prompt constants
UPDATE = "\nWhich device would you like to update "
QUIT = "(enter x to quit)? "
NEW_IP = "What is the new IP address (111.111.111.111) "
SORRY = "Sorry, that is not a valid IP address\n"

def load_equipment(file_path):
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_equipment(file_path, equipment_dict):
    with open(file_path, "w") as file:
        json.dump(equipment_dict, file)

def is_valid_ip(ip_address):
    parts = ip_address.split(".")
    if len(parts) != 4:
        return False
    for part in parts:
        try:
            num = int(part)
            if num < 0 or num > 255:
                return False
        except ValueError:
            return False
    return True

def getValidDevice(routers, switches):
    validDevice = False
    while not validDevice:
        device = input(UPDATE + QUIT).lower()
        if device in routers.keys():
            return device
        elif device in switches.keys():
            return device
        elif device == 'x':
            return device
        else:
            print("That device is not in the network inventory.")

def getValidIP(invalidIPCount, invalidIPAddresses):
    validIP = False
    while not validIP:
        ipAddress = input(NEW_IP)
        octets = ipAddress.split('.')
        for byte in octets:
            byte = int(byte)
            if byte < 0 or byte > 255:
                invalidIPCount += 1
                invalidIPAddresses.append(ipAddress)
                print(SORRY)
                break
        else:
            return ipAddress, invalidIPCount

def main():
    try:
        routers = load_equipment(EQUIP_R_FILE)
        switches = load_equipment(EQUIP_S_FILE)
    except Exception as e:
        print("Error loading equipment data:", e)
        return

    updated = {}
    invalidIPAddresses = []
    devicesUpdatedCount = 0
    invalidIPCount = 0
    quitNow = False
    validIP = False

    print("Network Equipment Inventory\n")
    print("\tequipment name\tIP address")
    for router, ipa in routers.items():
        print("\t" + router + "\t\t" + ipa)
    for switch, ipa in switches.items():
        print("\t" + switch + "\t\t" + ipa)

    while not quitNow:
        device = getValidDevice(routers, switches)
        if device == 'x':
            quitNow = True
            break
        ipAddress, invalidIPCount = getValidIP(invalidIPCount, invalidIPAddresses)
        if 'r' in device:
            routers[device] = ipAddress
        else:
            switches[device] = ipAddress
        devicesUpdatedCount += 1
        updated[device] = ipAddress
        print(device, "was updated; the new IP address is", ipAddress)

    print("\nSummary:\n")
    print("Number of devices updated:", devicesUpdatedCount)

    try:
        save_equipment(UPDATED_FILE, updated)
        print("Updated equipment written to file 'updated.txt'")
    except Exception as e:
        print("Error saving updated equipment data:", e)

    try:
        save_equipment(INVALID_FILE, invalidIPAddresses)
        print("List of invalid addresses written to file 'invalid.txt'")
    except Exception as e:
        print("Error saving invalid addresses data:", e)

if __name__ == "__main__":
    main()
