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
        return

    # Assuming create_profile.py is in the same directory as main.py
    create_profile_script = os.path.join(os.path.dirname(__file__), 'create_profile.py')
    create_profile_result = subprocess.run(["python", create_profile_script, proxies])
    
    if create_profile_result.returncode != 0:
        print("Error: create_profile.py failed.")
        return

    keyWord_file_path = os.path.join(desktop, 'keyword_data.txt')
    array_of_keyWord = fetch_proxies.read_keyWord_file_data(keyWord_file_path)
    
    if array_of_keyWord is None:
        print("Error: keyWords file missing.")
        return

    # Convert the array of keywords into a comma-separated string
    keywords_str = ",".join(array_of_keyWord)
    # Assuming profile_visiting.py is in the same directory as main.py
    profile_visiting_script = os.path.join(os.path.dirname(__file__), 'profile_visiting.py')
    profile_visiting_result = subprocess.run(["python", profile_visiting_script, keywords_str])
    
    if profile_visiting_result.returncode != 0:
        print("Error: profile_visiting.py failed.")
        return

if __name__ == "__main__":
    main()
