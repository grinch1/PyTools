from pandas._config.config import options
import scapy.all as scapy
import pandas as pd
import optparse


def get_args():
	parser = optparse.OptionParser()

	parser.add_option("-t","--target",dest="target",help="ip range to be scanned ")

	(options, arguments) = parser.parse_args()
	if not options.target:
		parser.error("[-] Please specify a target. use --help for more info")
	elif options.target:
		print('[+]Working on target request')
	return options 

def scan(ip):
	arp_request = scapy.ARP(pdst=ip)
	broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
	arp_ether = broadcast/arp_request
	ans_list = scapy.srp(arp_ether, timeout=1, verbose= False)[0]

	cli_list=[]
	for ans in ans_list:
		cli_dict = {"IP": ans[1].psrc, "MAC": ans[1].hwsrc}
		
		cli_list.append(cli_dict)
	return cli_list	

def print_result(scan_df):
	
	for ans in scan_df:
		df = pd.DataFrame()
		df = pd.DataFrame.from_dict(ans, orient='index')
		print("-----------------|---------------------|-------------")
		print(df.T)
		print("-----------------|---------------------|-------------")
		print(' ')

def run():
	options = get_args()
	scan_df_list = scan(options.target)
	print_result(scan_df_list)

run()


