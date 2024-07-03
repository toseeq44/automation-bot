import os
import subprocess
import pygetwindow as gw

def create_profile():
    print("hello from create profile function")

def find_window_and_maximize(window_title):
    windows = gw.getWindowsWithTitle(window_title)
    if windows:
        window = windows[0]
        if window.isMinimized:
            window.restore()
        window.activate()
        return True
    return False

def open_executable_on_desktop(executable_name, window_title):
    desktop_path = r"D:\adspower\AdsPower Global"
    exe_path = os.path.join(desktop_path, executable_name)

    if find_window_and_maximize(window_title):
        print(f"{window_title} window found and maximized.")
    else:
        if os.path.exists(exe_path):
            print(f"{window_title} window not found. Opening {executable_name}.")
            subprocess.Popen([exe_path])
            return True
        else:
            print(f"Error: {executable_name} not found at the specified path.")
            return False

if __name__ == "__main__":
    executable_name = "AdsPower Global.exe"
    window_title = "AdsPower"
    
    adsPower_respons = open_executable_on_desktop(executable_name, window_title)
    if adsPower_respons:
        create_profile()
    else:
        open_executable_on_desktop(executable_name, window_title)
