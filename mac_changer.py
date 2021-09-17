import subprocess
import optparse
import re

def changer(interface, new_mac):
	print("[+]Changing "+ options.interface + " to "+ options.new_mac)

	subprocess.call(["ifconfig",options.interface,'down'])
	print("[+]"+ interface+ " down")
	subprocess.call(["ifconfig",options.interface,"hw","ether", options.new_mac])
	print("[+]"+ "Setting new MAC")
	subprocess.call(["ifconfig",options.interface,'up'])
	print("[+]"+ interface+ " up")
	print("[!]Done")


def get_args():
	parser = optparse.OptionParser()

	parser.add_option("-i","--interfaces",dest="interface",help="interface to change its MAC")
	parser.add_option("-m","--mac",dest="new_mac",help="new MAC ")

	(options, arguments) = parser.parse_args()
	if not options.interface:
		parser.error("[-] Please specify an interface, use --help for more info")
	elif not options.new_mac:
		parser.error("[-] Please specify a MAC address, use --help for more info")
	return options	

def mac_check():
	check = options.new_mac[:2]
	check = int(check)
	
	if check % 2 == 0:
		print("[+]MAC is valid")
		
	if check % 2 != 0:
		print("[-]The first therm of the MAC address must be an even(MAC did not changed)") 
		


def get_mac(interface):
	result = subprocess.check_output(["ifconfig", interface])
	search = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", result.decode())
	if search:
		return search.group(0)
	else: 
		print("Could not read MAC address")


options = get_args()

mac_check()

mac = get_mac(options.interface)
print ("Current MAC = " + str(mac))

changer(options.interface, options.new_mac)
mac = get_mac(options.interface)
if mac == options.new_mac:
	print("[!] MAC address succefully changed to:  " + mac)