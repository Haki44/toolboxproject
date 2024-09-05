import subprocess

def get_password_policy():
    """Retrieve and display password policy information."""
    # Prompt the user for the target IP address
    target_ip = input("Enter the target IP address: ")

    # Check if the target IP address is provided
    if not target_ip:
        print("Target IP address is required. Exiting.")
        return

    # Construct the enum4linux command
    command = ["enum4linux", "-P", target_ip]

    # Run the enum4linux command
    print("Running enum4linux to retrieve password policy information...")
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print("Error:", e)
        return

if __name__ == "__main__":
    get_password_policy()
