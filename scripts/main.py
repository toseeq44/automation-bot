import os
import fetching_files_data
import subprocess
import threading
import keyboard
import time

# Variable to control the bot's running state
bot_running = True

def esc_listener():
    global bot_running
    while bot_running:
        if keyboard.is_pressed('esc'):
            print("ESC key pressed. Stopping the bot...")
            bot_running = False
            break
        time.sleep(0.1)

def run_subprocess(script, args):
    global bot_running
    process = subprocess.Popen(["python", script, args])
    while bot_running and process.poll() is None:
        time.sleep(0.1)
    if not bot_running:
        process.terminate()
        process.wait()
        return False
    return process.returncode == 0

def main():
    global bot_running

    # Start the ESC key listener thread
    listener_thread = threading.Thread(target=esc_listener)
    listener_thread.start()

    desktop = r"C:\Users\tosee\OneDrive\Desktop"
    file_path = os.path.join(desktop, 'proxy_data.txt')
    proxies = fetching_files_data.read_and_cut_first_proxy(file_path)
    print(f"proxie : {proxies}")
    
    if proxies is None:
        print("Error: No proxies found.")
        bot_running = False
        return

    create_profile_script = os.path.join(os.path.dirname(__file__), 'create_profile.py')
    if not run_subprocess(create_profile_script, proxies):
        print("Error: create_profile.py failed or stopped by user.")
        bot_running = False
        return

    keyWord_file_path = os.path.join(desktop, 'keyword_data.txt')
    array_of_keyWord = fetching_files_data.read_keyWord_file_data(keyWord_file_path)
    
    if array_of_keyWord is None:
        print("Error: keyWords file missing.")
        bot_running = False
        return

    keywords_str = ",".join(array_of_keyWord)
    profile_visiting_script = os.path.join(os.path.dirname(__file__), 'profile_visiting.py')
    if not run_subprocess(profile_visiting_script, keywords_str):
        print("Error: profile_visiting.py failed or stopped by user.")
        bot_running = False
        return

    bot_running = False  # Ensure the bot stops after completing the tasks

    # Wait for the listener thread to finish
    listener_thread.join()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        input("Press Enter to close...")
