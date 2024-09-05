import subprocess
from art import tprint
from scripts.test_pwd import test_pwd
from scripts.scan_vuln import scan_vulnerabilities
from scripts.hostdiscovery import exechostdicover
from scripts.scan_ports import portscan
from scripts.servicediscovery import Execservicedis
from scripts.udpscan import scan_udp
from scripts.user_sys import Exec_enum
from scripts.enumpasswordpolicy import get_password_policy
from scripts.enumerate_subdomains import subdomenum
from scripts.osdiscovery import Os_discovery
from scripts.scanforcve import scan_for_cves
from scripts.vulnScan import scan_vuln
from scripts.malwarescan import run_nmap_malware_script


def exploitation_menu():
    print("\n     EXPLOITATION MENU :")
    print("         [1] - Scan for exploitable CVEs")
    print("         [2] - Scan Vulnerabilities on a web server")
    print("         [3] - Scan for malware")
    print("         [0] - Back to main menu\n")

    choix = input("Veuillez choisir une option: ")

    if choix == "1":
        target = input("Please enter the target IP address or domain to scan for exploitable CVEs: ")
        scan_for_cves(target)
    elif choix == "2":
        target = input("Enter the target domain or IP address: ")
        port = input("Enter the port number to scan (press Enter for default): ")
        if not port:
            port = "80"  # Default port (e.g., HTTP)
        scan_vuln(target, port)
    elif choix == "3":
        target_ip = input("Enter the target IP address: ").strip()
        run_nmap_malware_script(target_ip)
    elif choix == "0":
        menu()
    else:
        print("Invalid option.")
        input("\nPress Enter to return to the menu.")
        exploitation_menu()

    input("\nPress Enter to return to the menu.")
    exploitation_menu()

def network_scanning_menu():
    print("\n     NETWORK SCANNING MENU :")
    print("         [1] - Network scan for host discovery")
    print("         [2] - Scan Open TCP Ports")
    print("         [3] - Discover each service per port")
    print("         [4] - Scan UDP Ports and Service")
    print("         [0] - Back to main menu\n")
    
    choix = input("Veuillez choisir une option: ")

    if choix == "1":
        target = input("Veuillez entrer l'adresse IP ou le nom de domaine à scanner pour la découverte d'hôtes: ")
        print(f"Scanning network for host discovery on target: {target}")
        exechostdicover()
    elif choix == "2":
        target = input("Veuillez entrer l'adresse IP ou le nom de domaine à scanner pour les ports TCP ouverts: ")
        portscan(target)  # Appel à la fonction de scan des ports
    elif choix == "3":
        target = input("Veuillez entrer l'adresse IP ou le nom de domaine à scanner pour découvrir les services par port: ")
        Execservicedis(target)
    elif choix == "4":
        target = input("Veuillez entrer l'adresse IP ou le nom de domaine à scanner pour les ports UDP: ")
        scan_udp()
    elif choix == "0":
        menu()
    else:
        print("Option non valide.")
        input("\nAppuyez sur Entrée pour retourner au menu.")
        network_scanning_menu()

    input("\nAppuyez sur Entrée pour retourner au menu.")
    network_scanning_menu()

def enumeration_menu():
    print("\n     ENUMERATION MENU :")
    print("         [1] - User and system enumeration")
    print("         [2] - Password Policy Information")
    print("         [3] - Enumerate Subdomains")
    print("         [4] - OS Discovery")
    print("         [0] - Back to main menu\n")

    choix = input("Veuillez choisir une option: ")

    if choix == "1":
        Exec_enum()
    elif choix == "2":
        get_password_policy()
    elif choix == "3":
        domain = input("Veuillez entrer le domaine pour énumérer les sous-domaines: ")
        subdomenum(domain)
    elif choix == "4":
       target = input("Enter the target IP address for OS discovery: ")
       Os_discovery(target)
    elif choix == "0":
        menu()
    else:
        print("Option non valide.")
        input("\nAppuyez sur Entrée pour retourner au menu.")
        enumeration_menu()

    input("\nAppuyez sur Entrée pour retourner au menu.")
    enumeration_menu()

def menu():
    print("\n     Toolbox MENU :")
    print("         [1] - NETWORK SCANNING")
    print("         [2] - Scan de vulnérabilités")
    print("         [3] - ENUMERATION")
    print("         [4] - EXPLOITATION")
    print("         [5] - Test d'authentification")
    print("         [6] - Analyse de la sécurité des mots de passe\n")
    print("         [7] - Générer un rapport\n")

    choix = input("Veuillez choisir une option: ")

    if choix == "1":
        network_scanning_menu()
    elif choix == "2":
        target = input("Veuillez entrer l'adresse IP ou le nom de domaine à scanner pour les vulnérabilités: ")
        scan_vulnerabilities(target)
        input("\nAppuyez sur Entrée pour retourner au menu.")
        menu()
    elif choix == "3":
        enumeration_menu()
    elif choix == "4":
        exploitation_menu()
    elif choix == "5":
        test_pwd()
        input("\nAppuyez sur Entrée pour retourner au menu.")
        menu()
    elif choix == "6":
        # Appelle la fonction appropriée pour générer un rapport
        input("\nAppuyez sur Entrée pour retourner au menu.")
        menu()
    else:
        print("Option non valide.")
        input("\nAppuyez sur Entrée pour retourner au menu.")
        menu()

if __name__ == "__main__":
    print("=" * 82)
    tprint("  Cyber Toolbox  ")
    print("=" * 82)
    print("                                   [version 1.0]")
    menu()
