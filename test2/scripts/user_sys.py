import subprocess
import re
import os
import ipaddress


def validate_ip(ip):
    """Validate IPv4 address."""
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False


def create_target_file(targets):
    """Create a file to store multiple target IP addresses."""
    with open("target.txt", "w") as file:
        for target in targets:
            file.write(target + "\n")


def Enum_usr_sys(target_ip, user_list_path=None):
    """Run enum4linux command to enumerate users and systems."""
    try:
        command = ["enum4linux", "-a", "-v", target_ip]

        if user_list_path:
            command.extend(["-U", user_list_path])
        else:
            command.append("-u")

        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing enum4linux command for {target_ip}: {e}")
    except FileNotFoundError:
        print("Error: enum4linux is not installed or not found in the system.")


def Exec_enum():
    """Execute user and system enumeration."""
    num_targets = int(input("Enter the number of target IP addresses: "))

    targets = []
    for i in range(num_targets):
        while True:
            target_ip = input(f"Enter target IP address {i + 1}: ")
            if validate_ip(target_ip):
                targets.append(target_ip)
                break
            else:
                print("Invalid IP address format. Please enter a valid IP address.")

    if not targets:
        print("No valid target IP addresses provided. Exiting.")
    else:
        if len(targets) > 1:
            create_target_file(targets)
            user_list_input = input("Do you have a list of users? (yes/no): ").lower()
            if user_list_input == "yes":
                print(f"Please make sure the userlist.txt file is in the current directory: {os.getcwd()}")
                user_list_path = "userlist.txt"
                if os.path.isfile(user_list_path):
                    with open("target.txt", "r") as file:
                        for line in file:
                            target_ip = line.strip()
                            Enum_usr_sys(target_ip, user_list_path)
                else:
                    print("User list file (userlist.txt) not found.")
            else:
                for target_ip in targets:
                    Enum_usr_sys(target_ip)
        else:
            target_ip = targets[0]
            user_list_input = input("Do you have a list of users? (yes/no): ").lower()
            if user_list_input == "yes":
                print(f"Please make sure the userlist.txt file is in the current directory: {os.getcwd()}")
                user_list_path = "userlist.txt"
                if os.path.isfile(user_list_path):
                    Enum_usr_sys(target_ip, user_list_path)
                else:
                    print("User list file (userlist.txt) not found.")
            else:
                Enum_usr_sys(target_ip)


if __name__ == "__main__":
    Exec_enum()