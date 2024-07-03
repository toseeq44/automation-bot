import os
import fetch_proxies
import subprocess

def main():
    # desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop') if os.name == 'nt' else os.path.join(os.path.expanduser('~'), 'Desktop')
    desktop = r"C:\Users\tosee\OneDrive\Desktop"
    file_path = os.path.join(desktop, 'proxy_data.txt')
    proxies = fetch_proxies.read_and_cut_first_proxy(file_path)
    print(f"proxie : {proxies}")
    
    if proxies is None:
        print("Error: No proxies found.")
    else:
        # Assuming create_profile.py is in the same directory as main.py
        create_profile_script = os.path.join(os.path.dirname(__file__), 'create_profile.py')
        subprocess.run(["python", create_profile_script])

if __name__ == "__main__":
    main()
