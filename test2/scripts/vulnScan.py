import subprocess

def scan_vuln(target, port):
    try:
        # Execute Nmap command
        nmap_command = ['nmap', '-sV', '--script', 'vuln', '-p', port, target]
        nmap_process = subprocess.Popen(nmap_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output, errors = nmap_process.communicate()

        # Check if there are any errors
        if errors:
            print("Error occurred while running Nmap:", errors)

        # Extract CVEs from output
        cves = []
        for line in output.split('\n'):
            if "CVE" in line:
                cves.append(line.strip())

        # Display found CVEs
        if cves:
            print("Found exploitable CVEs:")
            for cve in cves:
                print(cve)
        else:
            print("No exploitable CVEs found.")

    except Exception as e:
        print("An error occurred:", e)

# Example usage
if __name__ == "__main__":
    # Get target and port from user input
    target = input("Enter the target domain or IP address: ")
    port = input("Enter the port number to scan (press Enter for default): ")
    if not port:
        port = "80"  # Default port (e.g., HTTP)
    scan_vuln(target, port)