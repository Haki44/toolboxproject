import subprocess
import re

def validate_ip(ip):
    # Regular expression pattern for validating an IPv4 address
    ip_pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
    if re.match(ip_pattern, ip):
        return True
    else:
        return False

def discover_host(ip_address):
    active_hosts = []
    try:
        # Perform a ping scan using Nmap on a single IP address
        command = ["nmap", "-sn", ip_address]
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        # Parse the output to check if the host is active
        for line in result.stdout.split('\n'):
            if 'Nmap scan report for' in line:
                active_hosts.append(line.split()[-1])
        # Print the active host
        if active_hosts:
            print(f"Host {ip_address} is active.")
        else:
            print(f"No response from {ip_address}.")
    except subprocess.CalledProcessError as e:
        print("Error executing Nmap:", e)
    except Exception as e:
        print("An unexpected error occurred:", e)

def exechostdiscover():
    try:
        # Take IP address as input from the user
        while True:
            ip_address = input("Enter the IP address to scan (e.g., 192.168.1.1): ")
            if validate_ip(ip_address):
                break
            else:
                print("Invalid IP format. Please enter a valid IP address.")
        
        # Perform host discovery on the IP address
        discover_host(ip_address)
        print(f"{'-' * 69}SCAN DONE{'-' * 69}")

    except KeyboardInterrupt:
        print("\nProgram terminated by user.")
    except Exception as e:
        print("An unexpected error occurred:", e)

# Main entry point
if __name__ == "__main__":
    exechostdiscover()
