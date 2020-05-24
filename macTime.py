import subprocess as sp
import optparse as op
from logo import logo
import randmac
import random
import time
import re

def get_arguments():
    parser = op.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Your interface")
    parser.add_option("-t", "--time", dest="timeInv", help="Time interval")
    (options, arguments) = parser.parse_args()
    return options

def mac():
    return str(randmac.RandMac("00:00:00:00:00:00", True))

def changemac(interface):
    try:
        sp.call("ifconfig " + interface + " down", shell=True)
        sp.call("ifconfig " + interface + " hw ether " + mac(), shell=True)
        sp.call("ifconfig " + interface + " up", shell=True)
        ifconfig_result = sp.check_output("ifconfig " + interface, shell=True)
        mac_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result.decode("utf-8"))
        print("[+] Mac address has been changed to: " + mac_result.group(0))
    except:
        print("[!] Incorrect interface")

options = get_arguments()
logo()
euid = os.geteuid()

if euid != 0:
    print("Script not started as root. Running script with sudo..")
else:
    while True:
        changemac(options.interface)
        time.sleep(float(options.timeInv))  
