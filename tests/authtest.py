import paramiko

def test_ssh_authentication(ip, port, username, password):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(ip, port=port, username=username, password=password, timeout=10)
        print(f"Authentication successful for {username}:{password} on {ip}:{port}")
        return True
    except paramiko.AuthenticationException:
        print(f"Authentication failed for {username}:{password} on {ip}:{port}")
        return False
    except Exception as e:
        print(f"Error occurred: {e}")
        return False
    finally:
        ssh.close()

# Exemple d'utilisation
ip = "10.2.11.57"
port = 22
username = "passbolt"
password_list = ["password123", "admin", "root", "pocMDPA@2024"]

for password in password_list:
    result = test_ssh_authentication(ip, port, username, password)
    if result:
        break
