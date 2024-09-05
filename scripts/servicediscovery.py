import nmap

def Execservicedis(target):
    nm = nmap.PortScanner()
    scan_info = nm.scan(target, arguments='-sV -Pn -p-')  # Scan all ports

    print(f"Discovering services for target: {target}")
    for port, state in scan_info['scan'][target]['tcp'].items():
        if state['state'] == 'open':
            service_name = state.get('name', '')
            service_version = state.get('version', '')
            print(f"Port : {port} State : {state['state']} Service : {service_name} ({service_version})")

if __name__ == "__main__":
    target = input("Please enter the target (IP or hostname) to discover services: ")
    Execservicedis(target)
