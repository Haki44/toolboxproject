import subprocess
import re

def validate_cidr(cidr):
    # Regular expression pattern for CIDR notation
    cidr_pattern = r'^(\d{1,3}\.){3}\d{1,3}/\d{1,2}$'
    if re.match(cidr_pattern, cidr):
        return True
    else:
        return False

def discover_hosts(network_cidr):
    active_hosts = []
    try:
        # Perform a ping scan using Nmap
        command = ["nmap", "-sn", network_cidr]
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        # Parse the output to extract active hosts
        for line in result.stdout.split('\n'):
            if 'Nmap scan report for' in line:
                active_hosts.append(line.split()[-1])
        # Print the active hosts
        print("Active hosts are:")
        for host in active_hosts:
            print(host)
    except subprocess.CalledProcessError as e:
        print("Error executing Nmap:", e)
    except Exception as e:
        print("An unexpected error occurred:", e)

def exechostdicover():
    try:
        # Take network CIDR as input from the user
        while True:
            network_cidr = input("Enter the network in CIDR notation (e.g., 192.168.1.0/24): ")
            if validate_cidr(network_cidr):
                break
            else:
                print("Invalid CIDR format. Please enter a valid CIDR notation.")
        print(
            f'ACCORDING TO YOUR NETWORK THIS SCAN CAN BE RELATIVELY LONG GAIN IN TIME BY OPENING A NEW TERMINAL AN CONTINUE THROUGH')
        print(f" {'-'*56} SEGMENT YOUR NETWORK FOR RAPID SCAN{'-'*56}")
        # Perform host discovery
        discover_hosts(network_cidr)
        print(f"{'-' * 69}SCAN DONE{'-' * 69}")

    except KeyboardInterrupt:
        print("\nProgram terminated by user.")
    except Exception as e:
        print("An unexpected error occurred:", e)

# Main entry point
if __name__ == "__main__":
    exechostdicover()
