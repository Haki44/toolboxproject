import subprocess
from art import tprint
import sys
from scripts.scan_ports import scan_ports_services_os
from scripts.vuln_exploit import scan_website
from scripts.test_pwd import test_pwd
from scripts.scan_vuln import scan_vulnerabilities
from scripts.auth_test import authentification_testing
from scripts.exec_post_exploit import exec_post_exploit

def menu():
    # Affiche le menu
    print("\n     Menu toolbox :\n")
    print("             [1] - Scan de ports")
    print("             [2] - Scan de vulnérabilités")
    print("             [3] - Exploitation de vulnérabilités")
    print("             [4] - Test d'authentification")
    print("             [5] - Post exploitation")
    print("             [6] - Analyse de la sécurité des mots de passe")
    print("             [7] - Générer un rapport\n")

    print("         [Q] - Quitter\n")

    choix = input("Veuillez choisir une option: ")

    # Vérifie le choix de l'utilisateur
    if choix == "1":
        scan_ports_services_os()
        input("Appuyez sur entrer pour retourner au menu")
        menu()
    elif choix == "2":
        scan_vulnerabilities()
        input("Appuyez sur entrer pour retourner au menu")
        menu()
    elif choix == "3":
        scan_website()
        input("Appuyez sur entrer pour retourner au menu")
        menu()
    elif choix == "4":
        authentification_testing()
        input("Appuyez sur entrer pour retourner au menu")
        menu()
    elif choix == "5":
        exec_post_exploit()
        input("Appuyez sur entrer pour retourner au menu")
        menu()
    elif choix == "6":
        test_pwd()
        input("Appuyez sur entrer pour retourner au menu")
        menu()
    elif choix == "7":
        print("Script en cours de développement")
        input("Appuyez sur entrer pour retourner au menu")
        menu()
    elif choix.upper() == "Q":
        print("Script terminé")
        sys.exit()
    else:
        print("Option non valide.")
        menu()

if __name__ == "__main__":
    # Affichage de l'entête du menu
    print("=" * 82)
    tprint("  Cyber Toolbox  ")
    print("=" * 82)
    print("                                   [version 1.0]")
    menu()
