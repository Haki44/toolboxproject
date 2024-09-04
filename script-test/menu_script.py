import subprocess
from art import tprint
from scripts.test_pwd import test_pwd
from scripts.scan_vuln import scan_vulnerabilities
from scripts.auth_test import authentification_testing

def menu():
    # Affiche le menu
    print("\n     Menu toolbox :")
    print("         [1] - Scan de ports")
    print("         [2] - Scan de vulnérabilités")
    print("         [3] - Exploitation de vulnérabilités")
    print("         [4] - Test d'authentification")
    print("         [5] - Analyse de la sécurité des mots de passe")
    print("         [6] - Générer un rapport\n")

    choix = input("Veuillez choisir une option: ")

    # Vérifie le choix de l'utilisateur
    if choix == "1":
        subprocess.run(['python3', 'script_n1.py'])  # Exécuter le script n1 avec le nom de fichier en argument
    elif choix == "2":
        scan_vulnerabilities()
        input("Appuyez sur entrer pour retourner au menu")
        menu()
    elif choix == "4":
        authentification_testing()
        input("Appuyez sur entrer pour retourner au menu")
        menu()
    elif choix == "5":
        test_pwd()
        input("Appuyez sur entrer pour retourner au menu")
        menu()
    else:
        print("Option non valide.")

if __name__ == "__main__":
    # Affichage de l'entête du menu
    print("=" * 82)
    tprint("  Cyber Toolbox  ")
    print("=" * 82)
    print("                                   [version 1.0]")
    menu()
