import subprocess
import requests
import re
import sys
from colorama import Fore, Style


def scan_vulnerabilities():
    """ Point d'entrée pour l'analyse des vulnérabilités """

    print("\n" + "╔" + "═" * 39 + "╗")
    print("║ Analyse des vulnérabilités avec Nikto ║")
    print("╚" + "═" * 39 + "╝")

    url = input("\n\033[1;36mEntrez l'URL à scanner : \033[0m")
    
    if not is_valid_url(url):
        print(f"{Fore.RED}>>> [!] Format de l'URL incorrect{Style.RESET_ALL}")
        sys.exit()

    check_server(url)
    check_robots_txt(url)


def is_valid_url(url):
    """ Vérifie si le format de l'URL est valide """

    regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// ou https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domaine...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'  # ...ou ipv4
        r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'  # ...ou ipv6
        r'(?::\d+)?'  # port optionnel
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    return re.match(regex, url) is not None


def check_server(url):
    """ Vérifie les informations sur le serveur web """

    print("\n[╦] \033[1;36mAnalyse du serveur Web\033[0m")
    try:
        response = requests.get(url)
        server = response.headers.get("Server", "Non disponible")
        x_powered_by = response.headers.get("X-Powered-By", "Non disponible")
        content_encoding = response.headers.get("Content-Encoding", "Non supporté")
        print(f" ╠═[-] Serveur Web : {server}")
        print(f" ╠═[-] Propulsé par : {x_powered_by}")
        print(f" ╠═[-] Support de la compression : {content_encoding}")
        check_version_leak(response.headers)
        check_redirection(response)
        check_basic_auth(response)
        check_security_headers(url)
    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}>>> [-] Erreur lors de la requête : {e}{Style.RESET_ALL}")
        sys.exit(1)


def check_version_leak(headers):
    """ Vérifie si les en-têtes contiennent des versions de logiciels """
    
    version_regex = re.compile(r"\d+\.\d+(\.\d+)?")
    found_version = False
    
    for header, value in headers.items():
        match = version_regex.search(value)
        if match:
            found_version = True
            print(f" ╠═[\033[1;31m!\033[0m] Fuite de version dans '{header}' : \033[1;31m{match.group(0)}\033[0m")
    
    if not found_version:
        print(" ╠═[-] Pas de fuite de version détectée")


def check_redirection(response):
    """ Vérifie si l'URL cible redirige vers une autre URL """

    if response.status_code in [301, 302]:
        print(f" ╠═[-] Redirection vers : {response.headers.get('Location')}")
    else:
        print(" ╠═[-] Aucune redirection détectée")


def check_basic_auth(response):
    """ Vérifie si l'URL cible est protégée par une authentification basique HTTP """

    if response.status_code == 401:
        print(f" ╠═[-] URL protégée par une authentification basique HTTP")
        print(f"[╩]")
    else:
        print(" ╠═[-] Pas d'authentification basique détectée")
        print("[╩]")


def check_security_headers(url):
    """ Vérifie la présence d'en-têtes de sécurité courants """

    headers = {
        "X-Frame-Options": "anti-clickjacking",
        "X-XSS-Protection": "XSS protection",
        "X-Content-Type-Options": "MIME-sniffing"
    }
    
    print("\n[╦] \033[1;36mVérification des en-têtes de sécurité\033[0m")
    
    try:
        response = requests.get(url, headers=headers)
        for header, description in headers.items():
            if header not in response.headers:
                print(f" ╠═[\033[1;31m!\033[0m] Absence de l'en-tête {description} : \033[1;31m{header}\033[0m")
            else:
                print(f" ╠═[-] Présence de l'en-tête {description} : \033[1;32m{header}\033[0m")
        print("[╩]")
    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}>>> [-] Erreur lors de la vérification des en-têtes de sécurité : {e}{Style.RESET_ALL}")


def check_robots_txt(url):
    """ Vérifie l'accessibilité du fichier robots.txt """

    print("\n[╦] \033[1;36mVérification du fichier robots.txt\033[0m")
    
    try:
        r = requests.get(f"{url}/robots.txt")
        if r.status_code == 200:
            print(f" ╠═[-] robots.txt est accessible publiquement")
            print(f" ╠═[-] Contenu de robots.txt :\n{r.text}")
        else:
            print(f" ╠═[\033[1;31m!\033[0m] robots.txt n'est pas accessible publiquement")
        print("[╩]\n")
    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}>>> [-] Erreur lors de l'accès à robots.txt : {e}{Style.RESET_ALL}")


if __name__ == "__main__":
    scan_vulnerabilities()
