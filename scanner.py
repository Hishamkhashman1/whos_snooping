from scapy.all import ARP, Ether, srp
import socket
import ipaddress
import requests


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
            "mac": received.hwsrc,
            "vendor": get_vendor(received.hwsrc),
            "hostname": get_hostname(received.psrc)
            })

    return devices



def is_random_mac(mac):
    first_octet = int(mac.split(":")[0], 16)
    return bool(first_octet & 0b10)



def get_hostname(ip):
    try:
        return socket.gethostbyaddr(ip)[0]
    except Exception:
        return None

def load_oui_db(path="oui.txt"):
    db = {}
    with open(path, "r", errors="ignore") as f:
        for line in f:
            if "(hex)" in line:
                parts = line.split()
                prefix = parts[0].replace("-", ":").lower()
                vendor = " ".join(parts[2:])
                db[prefix] = vendor
    return db

OUI_DB = load_oui_db()

def get_vendor(mac):
    prefix = mac.lower()[0:8]
    return OUI_DB.get(prefix, "Unknown")


if __name__ == "__main__":
    target = target = get_local_subnet()
    devices = scan_network(target)

    print("Devices on the network:")
    for device in devices:
        print(f"{device['ip']}  ->  {device['mac']}")
