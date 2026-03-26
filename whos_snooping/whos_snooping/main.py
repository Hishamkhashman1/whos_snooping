from scanner import scan_network, get_local_subnet

def main():
    target = get_local_subnet()
    print(f"Scanning network: {target}\n")

    devices = scan_network(target)

    if not devices:
        print("No devices found.")
        return

    print("Devices on the network:")
    for device in devices:
        print(f"{device['ip']}  ->  {device['mac']}  ({device['vendor']})")


if __name__ == "__main__":
    main()
