from scapy.all import ARP, Ether, srp
import socket
import ipaddress

def get_local_subnet():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    local_ip = s.getsockname()[0]
    s.close()

    network = ipaddress.ip_network(local_ip + "/24", strict=False)
    return str(network)

def scan_network(target_ip):

    # Create ARP request
    arp = ARP(pdst=target_ip)

    # Create Ethernet frame
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")

    # Stack them
    packet = ether / arp

    # Send and receive packets
    result = srp(packet, timeout=2, verbose=False)[0]

    devices = []
    for sent, received in result:
        devices.append({
            "ip": received.psrc,
            "mac": received.hwsrc
        })

    return devices


if __name__ == "__main__":
    target = target = get_local_subnet()
    devices = scan_network(target)

    print("Devices on the network:")
    for device in devices:
        print(f"{device['ip']}  ->  {device['mac']}")
