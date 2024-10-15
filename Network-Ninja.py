from scapy.all import ARP, Ether, srp
import sys

def scan(ip_range):
    """Scan the specified IP range for active devices. Let's find those sneaky devices lurking on the network!"""
    arp = ARP(pdst=ip_range)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")  # Broadcasting like it's a party invitation!
    packet = ether / arp

    try:
        # Send the packet and capture the response
        result = srp(packet, timeout=2, verbose=0)
    except Exception as e:
        print(f"Error sending ARP requests: {e}. Probably my fault... or the universe's.")
        return []

    clients = []
    for sent, received in result[0]:
        clients.append({'ip': received.psrc, 'mac': received.hwsrc})

    return clients

def print_results(clients):
    """Print the results of the scan in a formatted way. Time to unveil the devices!"""
    print("Available devices in the network:")
    print("IP Address\t\tMAC Address")
    print("-" * 40)
    for client in clients:
        print(f"{client['ip']}\t{client['mac']}")  # The ultimate reveal! 🎉

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 ip_scanner.py <ip_range>")
        print("Example: python3 ip_scanner.py 192.168.1.0/24")  # Your ticket to the device show!
        sys.exit(1)

    ip_range = sys.argv[1]
    clients = scan(ip_range)

    if clients:
        print_results(clients)
    else:
        print("No devices found in the specified IP range. It's a ghost town out here!")
