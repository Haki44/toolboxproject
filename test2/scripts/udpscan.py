import nmap

def scan_udp(target):
    scanner = nmap.PortScanner()  # Initialize nmap PortScanner object
    scanner.scan(hosts=target, arguments='-sU -T4')  # Perform UDP scan with aggressive timing
    for host in scanner.all_hosts():
        print(f"Host: {host}")
        for proto in scanner[host].all_protocols():
            print(f"Protocol: {proto}")
            ports = scanner[host][proto].keys()
            for port in ports:
                state = scanner[host][proto][port]['state']
                print(f"Port {port} ({proto}): {state}")

if __name__ == "__main__":
    target = input("Please enter the target IP or hostname for UDP scan: ")
    scan_udp(target)
