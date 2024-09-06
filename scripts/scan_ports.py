import nmap
import socket
from halo import Halo

def scan_ports():
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
            print(f"\033[1;31mErreur : Impossible de résoudre le domaine {target}\033[0m")
            return None

    def scan_ports_services_os():
        print("\n" + "╔" + "═" * 28 + "╗")
        print("║ Scan des Ports et Services ║")
        print("╚" + "═" * 28 + "╝")

        target = input("\n\033[1;36mEntrez l'adresse IP ou le domaine à scanner : \033[0m")
        nm = nmap.PortScanner()

        # Résolution du domaine si nécessaire
        ip_address = resolve_domain(target)
        if not ip_address:
            return  # Arrête si la résolution échoue

        print(f"\n[+] \033[1;33mScan de {target} ({ip_address}) pour les ports, services, et informations d'OS...\033[0m")

        # Utilisation de Halo pour afficher un loader pendant le scan
        with Halo(text='Scan en cours...', spinner='dots'):
            try:
                # Scan avec des scripts NSE pour obtenir plus d'informations
                nm.scan(ip_address, arguments='-sV --script=banner,http-enum -Pn')

                # Affichage des résultats pour chaque hôte trouvé
                for host in nm.all_hosts():
                    print(f"\n\033[1;32mHôte : {host} ({nm[host].hostname()})\033[0m")
                    print(f"État : {nm[host].state()}")

                    # Liste des ports ouverts
                    if 'tcp' in nm[host]:
                        print("\033[1;36mPorts ouverts et services détectés :\033[0m")
                        for port in nm[host]['tcp']:
                            port_info = nm[host]['tcp'][port]
                            print(f"  Port {port}: {port_info['name']} "
                                  f"(Produit: {port_info.get('product', 'N/A')} "
                                  f"Version: {port_info.get('version', 'N/A')})")

                            # Affichage des résultats des scripts NSE
                            if 'script' in port_info:
                                for script_name, output in port_info['script'].items():
                                    print(f"    Résultat du script {script_name} :")
                                    print(f"    {output}")
                    else:
                        print("Aucun port ouvert trouvé.")

                    # Déduire l'OS à partir des bannières et des services
                    if 'osclass' in nm[host]:
                        for osclass in nm[host]['osclass']:
                            print(f"OS détecté : {osclass['osfamily']} {osclass['osgen']}")
            except Exception as e:
                print(f"\033[1;31mUne erreur s'est produite : {e}\033[0m")
    
    scan_ports_services_os()

if __name__ == "__main__":
    scan_ports()