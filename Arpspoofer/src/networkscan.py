import scapy.all as scapy

req = scapy.ARP()

req.pdst = "192.168.0.1/24"
broadcast = scapy.ARP()


broadcast.dst = "ff:ff:ff:ff:ff:ff"

req_broadcast = broadcast / req
clients = scapy.srp(req_broadcast, timeout = 10, verbose = 1)[0]
for elm in clients:
    print(elm[1].psrc + "  " + elm[1].hwsrc)
