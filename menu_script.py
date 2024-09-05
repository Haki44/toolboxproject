import subprocess
from art import tprint
from scripts.scan_ports import scan_ports_services_os
from scripts.vuln_exploit import scan_website


def menu():
    print("\n     Toolbox MENU :")
    print("         [1] - Scan de ports et services")
    print("         [2] - Scan de vulnérabilités")
    print("         [3] - Exploitation")
    print("         [4] - Test d'authentification")
    print("         [5] - Analyse de la sécurité des mots de passe")
    print("         [6] - Générer un rapport\n")

    choix = input("Veuillez choisir une option: ")

    if choix == "1":
        target = input("Entrez l'adresse IP ou le domaine à scanner : ")
        scan_ports_services_os(target)
    elif choix == "2":
        target = input("Veuillez entrer l'adresse IP ou le nom de domaine à scanner pour les vulnérabilités: ")
        scan_vulnerabilities(target)
        input("\nAppuyez sur Entrée pour retourner au menu.")
        menu()
    elif choix == "3":
        target_url = input("Entrez l'URL de la cible à scanner : ")
        scan_website(target_url)
    elif choix == "4":
        print("Script en cours ...")
        input("Appuyez sur entrer pour retourner au menu")
        menu()  
    elif choix == "5":
        print("Script en cours ...")
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
