import subprocess
import re

def list_clients():
    try:
        result = subprocess.run("incus config trust list", shell=True, capture_output=True, text=True, check=True)
        output = result.stdout.strip()
        client_list = {}
        rows = re.findall(r"\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|", output, re.MULTILINE)
        for row in rows:
            name, _, _, fingerprint, _ = map(str.strip, row)
            if name and fingerprint:
                client_list[name] = fingerprint
        return client_list
    except subprocess.CalledProcessError as e:
        print(f"Error listing clients: {e}")
        return None

def remove_client(fingerprint):
    command = f'incus config trust remove {fingerprint}'
    try:
        subprocess.run(command, shell=True, check=True)
        print(f"Client with fingerprint {fingerprint} removed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error removing client with fingerprint {fingerprint}: {e}")

# Example usage:
if __name__ == "__main__":
    while True:
        clients = list_clients()
        if clients:
            print("List of clients and their fingerprints:")
            for index, (name, fingerprint) in enumerate(clients.items()):
                print(f"{index}: {name} - {fingerprint}")
            
            client_index = input("Enter the index of the client you want to remove, or 'q' to quit: ")
            if client_index.lower() == 'q':
                break
            try:
                client_index = int(client_index)
                if 0 <= client_index < len(clients):
                    fingerprint_to_remove = list(clients.values())[client_index]
                    remove_client(fingerprint_to_remove)
                else:
                    print("Invalid index. Please enter a valid index from the list.")
            except ValueError:
                print("Invalid input. Please enter a number.")
        else:
            print("No clients found in the trust list.")
