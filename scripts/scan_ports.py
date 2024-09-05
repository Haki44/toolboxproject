import nmap
import socket

def resolve_domain(target):
    """
    Résout un domaine en adresse IP.
    Si la cible est déjà une adresse IP, elle est retournée telle quelle.
    """
    try:
        # Essaye de résoudre le nom de domaine en adresse IP
        ip_address = socket.gethostbyname(target)
        return ip_address
    except socket.gaierror:
        print(f"Erreur : Impossible de résoudre le domaine {target}")
        return None

def scan_ports_services_os(target):
    # Initialisation du scanner Nmap
    nm = nmap.PortScanner()

    # Résolution du domaine si nécessaire
    ip_address = resolve_domain(target)
    if not ip_address:
        return  # Arrête si la résolution échoue

    print(f"[+] Scan de {target} ({ip_address}) pour les ports, services, et informations d'OS...")

    try:
        # Scan avec des scripts NSE pour obtenir plus d'informations
        # Nous incluons le script NSE "banner" et d'autres pouvant révéler l'OS
        nm.scan(ip_address, arguments='-sV --script=banner,http-enum -Pn')

        # Affichage des résultats pour chaque hôte trouvé
        for host in nm.all_hosts():
            print(f"Hôte : {host} ({nm[host].hostname()})")
            print(f"État : {nm[host].state()}")

            # Liste des ports ouverts
            if 'tcp' in nm[host]:
                print("Ports ouverts et services détectés :")
                for port in nm[host]['tcp']:
                    port_info = nm[host]['tcp'][port]
                    print(f"Port {port}: {port_info['name']} "
                          f"(Produit: {port_info.get('product', 'N/A')} "
                          f"Version: {port_info.get('version', 'N/A')})")

                    # Affichage des résultats des scripts NSE
                    if 'script' in port_info:
                        for script_name, output in port_info['script'].items():
                            print(f"Résultat du script {script_name}:")
                            print(output)
            else:
                print("Aucun port ouvert trouvé.")

            # Essayez de déduire l'OS à partir des bannières et des services
            if 'osclass' in nm[host]:
                for osclass in nm[host]['osclass']:
                    print(f"OS détecté : {osclass['osfamily']} {osclass['osgen']}")

    except Exception as e:
        print(f"Une erreur s'est produite : {e}")

if __name__ == "__main__":
    # Demande de la cible (IP ou domaine) à scanner
    target = input("Entrez l'adresse IP ou le domaine à scanner : ")
    scan_ports_services_os(target)
