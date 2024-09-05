import nmap
import socket

def portscan(target):
    nm = nmap.PortScanner()
    scan_info = nm.scan(target, arguments='-Pn')

    print(f"Scanning target: {target}")
    for port, state in scan_info['scan'][target]['tcp'].items():
        print(f"Port : {port} State : {state['state']}")

    print(f"{'-' * 50} SCAN DONE {'-' * 50}")

if __name__ == "__main__":
    target = input("Please enter the target (IP or hostname) for the port scan: ")
    portscan(target)
