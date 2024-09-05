import nmap

def Os_discovery(target):
    """Perform OS discovery using Nmap."""
    nm = nmap.PortScanner()
    scan_info = nm.scan(target, arguments='-Pn -O')  # Scan all ports and enable OS detection

    for host in scan_info['scan'].keys():
        os_info = scan_info['scan'][host].get('osmatch', [])
        if os_info:
            for os_dict in os_info:
                os_name = os_dict.get('name', '')
                accuracy = os_dict.get('accuracy', 0)
                print(f"OS : {os_name} (Accuracy: {accuracy}%)")

if __name__ == "__main__":
    target = input("Enter the target IP address for OS discovery: ")
    Os_discovery(target)
