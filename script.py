import os
import subprocess
import time
from tqdm import tqdm

# Fonction pour exécuter une commande et récupérer la sortie
def run_command(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    stdout, stderr = process.communicate()
    return stdout.decode(errors='ignore'), stderr.decode(errors='ignore')

# Fonction pour scanner les ports et services avec nmap
def scan_ports(target):
    command = f"nmap -sV -oX nmap_scan.xml {target}"
    stdout, stderr = run_command(command)
    return stdout, stderr

# Fonction pour détecter les vulnérabilités avec nmap NSE scripts
def detect_vulnerabilities(target):
    command = f"nmap --script vuln -oX nmap_vuln_scan.xml {target}"
    stdout, stderr = run_command(command)
    return stdout, stderr

# Fonction pour lancer un scan Nikto
def run_nikto(target):
    command = f"nikto -h {target} -o nikto_scan.txt"
    stdout, stderr = run_command(command)
    return stdout, stderr

# Fonction pour analyser les résultats de scan nmap
def parse_nmap_xml(file_path):
    import xml.etree.ElementTree as ET
    tree = ET.parse(file_path)
    root = tree.getroot()
    results = []
    
    for host in root.findall('host'):
        host_info = {}
        for address in host.findall('address'):
            host_info['ip'] = address.get('addr')
        for port in host.findall('ports/port'):
            port_info = {
                'portid': port.get('portid'),
                'service': port.find('service').get('name')
            }
            host_info.setdefault('ports', []).append(port_info)
        results.append(host_info)
    return results

# Fonction pour lire les résultats de Nikto
def parse_nikto_results(file_path):
    with open(file_path, 'r') as file:
        return file.read()

# Fonction pour générer un rapport HTML
def generate_html_report(data, output_file):
    target = data['target']
    scan_results = data['scan_results']
    vuln_results = data['vuln_results']
    nikto_results = data['nikto_results']
    
    template = f"""<!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Rapport de Vulnérabilités</title>
    </head>
    <body>
        <h1>Rapport de Vulnérabilités pour {target}</h1>
        
        <h2>Résultats du Scan des Ports et Services</h2>
        <ul>
            {''.join(
                f"<li><strong>IP: {host['ip']}</strong><ul>" + 
                ''.join(f"<li>Port: {port['portid']} - Service: {port['service']}</li>" for port in host['ports']) +
                "</ul></li>"
                for host in scan_results
            )}
        </ul>
        
        <h2>Résultats de la Détection de Vulnérabilités</h2>
        <ul>
            {''.join(
                f"<li><strong>IP: {host['ip']}</strong><ul>" + 
                ''.join(f"<li>Port: {port['portid']} - Service: {port['service']}</li>" for port in host['ports']) +
                "</ul></li>"
                for host in vuln_results
            )}
        </ul>

        <h2>Résultats du Scan Nikto</h2>
        <pre>{nikto_results}</pre>
    </body>
    </html>"""
    
    with open(output_file, 'w') as f:
        f.write(template)

# Main function
def main():
    target = input("Veuillez entrer l'IP ou l'URL cible : ")

    # Step 1: Scan ports and services
    print("Scanning ports and services...")
    with tqdm(total=100, desc="Scan des ports") as pbar:
        stdout, stderr = scan_ports(target)
        if stdout:
            pbar.update(100)
        else:
            pbar.close()
            print("Erreur lors du scan des ports:", stderr)
            return
    
    # Step 2: Detect vulnerabilities
    print("Detecting vulnerabilities...")
    with tqdm(total=100, desc="Détection des vulnérabilités") as pbar:
        stdout, stderr = detect_vulnerabilities(target)
        if stdout:
            pbar.update(100)
        else:
            pbar.close()
            print("Erreur lors de la détection des vulnérabilités:", stderr)
            return

    # Step 3: Run Nikto scan
    print("Running Nikto scan...")
    with tqdm(total=100, desc="Scan Nikto") as pbar:
        stdout, stderr = run_nikto(target)
        if stdout:
            pbar.update(100)
        else:
            pbar.close()
            print("Erreur lors du scan Nikto:", stderr)
            return
    
    # Step 4: Parse nmap results
    print("Parsing scan results...")
    scan_results = parse_nmap_xml('nmap_scan.xml')
    vuln_results = parse_nmap_xml('nmap_vuln_scan.xml')
    nikto_results = parse_nikto_results('nikto_scan.txt')
    
    # Combine results
    results = {
        'target': target,
        'scan_results': scan_results,
        'vuln_results': vuln_results,
        'nikto_results': nikto_results
    }
    
    # Step 5: Generate HTML report
    print("Generating HTML report...")
    generate_html_report(results, 'report.html')
    print("Report generated: report.html")

if __name__ == '__main__':
    main()
