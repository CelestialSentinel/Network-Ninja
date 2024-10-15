from scapy.all import ARP, Ether, srp
import sys
from tabulate import tabulate

def scan(ip_range):
    """Scanning active devices in the specified IP range"""
    arp = ARP(pdst=ip_range)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")  # Broadcasting
    packet = ether / arp

    try:
        # Send the packet and capture the response
        result = srp(packet, timeout=2, verbose=0)
    except Exception as e:
        print(f"Error sending ARP requests: {e}.")
        return []

    clients = []
    for sent, received in result[0]:
        clients.append({'IP Address': received.psrc, 'MAC Address': received.hwsrc})

    return clients

def print_results(clients):
    """Printing response in a tabular form"""
    if clients:
        print("Available devices in the network:")
        print(tabulate(clients, headers="keys", tablefmt="pretty"))
    else:
        print("No devices found.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 ip_scanner.py <ip_range>")
        print("Example: python3 ip_scanner.py 192.168.1.0/24")
        sys.exit(1)

    ip_range = sys.argv[1]
    clients = scan(ip_range)
    print_results(clients)
