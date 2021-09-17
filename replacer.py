import netfilterqueue
import scapy.all as scapy

def process(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer:
        if scapy_packet.haslayer(scapy.TCP).dport == 80:
            print("HTTP Request")
            print(scapy_packet.show())
            if ".exe"
        elif scapy_packet[scapy.TCP].sport == 80:
            print("HTTP Responset")
            print(scapy_packet.show())


    packet.accept()
 
 
queue = netfilterqueue.NetfilterQueue()
queue.bind(4, process)
queue.run()
