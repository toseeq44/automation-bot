import os
import subprocess
import pygetwindow as gw
import time
import pyautogui
import math
import random
import sys
import pyperclip

def move_mouse_in_circle(duration=5, radius=100):
    screen_width, screen_height = pyautogui.size()
    center_x, center_y = screen_width / 2, screen_height / 2

    start_time = time.time()
    while time.time() - start_time < duration:
        # Calculate current angle (in radians)
        current_time = time.time() - start_time
        angle = current_time * 2 * math.pi / duration  # Complete one circle in the given duration
        
        # Calculate x and y positions
        x = center_x + radius * math.cos(angle)
        y = center_y + radius * math.sin(angle)
        
        # Move the mouse to the calculated position
        pyautogui.moveTo(x, y, duration=0.1)
        time.sleep(0.01)  # Small sleep to avoid high CPU usage

def scroll_down_mouse(scrolls=5, delay=0.5):
    x, y = 500, 500
    pyautogui.moveTo(x, y)

    # Perform the scroll down action
    for _ in range(scrolls):
        pyautogui.scroll(-500)  # Negative value to scroll down
        time.sleep(delay)  # Wait for specified delay

def human_like_move_and_click(location):
    # Get the current position of the mouse
    current_x, current_y = pyautogui.position()
    
    # Calculate the distance and angle to the target location
    target_x, target_y = location
    distance = math.hypot(target_x - current_x, target_y - current_y)
    angle = math.atan2(target_y - current_y, target_x - current_x)
    
    # Move in small steps
    steps = int(distance / 10) + 1
    for i in range(steps):
        step_distance = distance / steps
        step_x = current_x + step_distance * math.cos(angle)
        step_y = current_y + step_distance * math.sin(angle)
        pyautogui.moveTo(step_x, step_y, duration=random.uniform(0.01, 0.03))
    
    # Move to the exact location with a slight random offset
    pyautogui.moveTo(target_x + random.uniform(-3, 3), target_y + random.uniform(-3, 3), duration=random.uniform(0.1, 0.3))
    
    # Click with a small random delay
    time.sleep(random.uniform(0.05, 0.15))
    pyautogui.click()
    time.sleep(random.uniform(0.05, 0.15))

def wait_and_click(image, timeout=180, check_interval=10, confidence=0.9):
    start_time = time.time()
    while time.time() - start_time < timeout:
        print("Checking for the image...")
        try:
            location = pyautogui.locateOnScreen(image, confidence=confidence)
            if location is not None:
                center_location = pyautogui.center(location)
                human_like_move_and_click(center_location)
                print(f"Image '{image}' located and clicked.")
                return True
        except Exception as e:
            print(f"An error occurred: {e}")
        time.sleep(check_interval)
    print(f"Image '{image}' could not be located after {timeout} seconds.")
    return False

def wait_for_image(image, timeout=180, check_interval=2, confidence=0.9):
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            location = pyautogui.locateOnScreen(image, confidence=confidence)
            if location is not None:
                print(f"Image '{image}' located.")
                return location
        except Exception as e:
            print(f"An error occurred: {e}")
        time.sleep(check_interval)
    print(f"Image '{image}' could not be located after {timeout} seconds.")
    return None



def create_profile(profile_creation_ok_but_img, app_lang_togleButon_img, WebRTC_Replac_but_img, proxy_advanced_but_img, adsPower_back_but_img, proxy_connection_success_img, proxy_connection_failed_img, check_proxy_button, Host_Port_img, new_profile_button, select_proxy_type, HTTPS_proxy_type_img, Socks5_proxy_type_img, current_proxy, attempts=5, delay_between_attempts=2):
    time.sleep(5)
    move_mouse_in_circle(2, 100)

# Step 1: Click the new profile button
    try:
        if wait_and_click(new_profile_button, timeout=180, check_interval=10, confidence=0.8):
            print("New profile button clicked successfully.")
    except pyautogui.ImageNotFoundException as e:
        print(e)
        return

    move_mouse_in_circle(10, 70)
    scroll_down_mouse(1)

#Step 2: Select proxy type
    try:
        if wait_and_click(select_proxy_type, timeout=180, check_interval=10, confidence=0.9):
            print("Proxy type selected successfully.")
    except pyautogui.ImageNotFoundException as e:
        print(e)
        return

    move_mouse_in_circle(3, 300)

# Step 3: Select HTTPS or SOCKS5 proxy
    for attempt in range(attempts):
        https_proxy_selection = wait_for_image(HTTPS_proxy_type_img, timeout=180, check_interval=2, confidence=0.9)
        socks5_proxy_selection = wait_for_image(Socks5_proxy_type_img, timeout=180, check_interval=2, confidence=0.85)
        
        if https_proxy_selection is not None or socks5_proxy_selection is not None:
            random_choice = random.randint(1, 2)
            if random_choice == 1 and https_proxy_selection is not None:
                proxy_type = pyautogui.center(https_proxy_selection)
                print("Selected HTTPS proxy type.")
            elif random_choice == 2 and socks5_proxy_selection is not None:
                proxy_type = pyautogui.center(socks5_proxy_selection)
                print("Selected SOCKS5 proxy type.")
            else:
                continue
            
            pyautogui.moveTo(proxy_type.x, proxy_type.y, duration=0.5)
            pyautogui.click(proxy_type.x, proxy_type.y)
            print("Proxy type selected successfully.")
            break
        else:
            print(f"Attempt {attempt + 1}: Proxy type button not found. Retrying...")
            time.sleep(delay_between_attempts)
    else:
        print("Proxy type button could not be found after multiple attempts.")
        return

    time.sleep(0.3)
    move_mouse_in_circle(3, 30)
    scroll_down_mouse(1)

    # Step 4: Enter proxy details
    pyperclip.copy(current_proxy)
    try:
        if wait_and_click(Host_Port_img, timeout=180, check_interval=10, confidence=0.7):
            pyautogui.hotkey('ctrl', 'v')
            print("Proxy details entered successfully.")
    except pyautogui.ImageNotFoundException as e:
        print(e)
        return

# Step 5: Check proxy connection
    try:
        if wait_and_click(check_proxy_button, timeout=180, check_interval=10, confidence=0.9):
            time.sleep(2)  # Wait for the result to appear
            move_mouse_in_circle(3, 10)
            
            con_fail = wait_for_image(proxy_connection_failed_img, timeout=10, check_interval=1, confidence=0.99)
            con_success = wait_for_image(proxy_connection_success_img, timeout=10, check_interval=1, confidence=0.99)
            #yahan if els cond ulti lagi hoi ha butt kam proper kr rahi kh jb proxy con suces ho ga tbhi scroll ni to back
            if con_fail is not None:
                scroll_down_mouse(1)
                print("Proxy connected successfully.")
            elif con_success is not None:
                move_mouse_in_circle(3, 10)
                wait_and_click(adsPower_back_but_img, timeout=180, check_interval=10, confidence=0.9)
                print("Proxy connection failed. Going back.")
    except Exception as e:
        print(f"An error occurred: {e}")
        return 
    
    move_mouse_in_circle(3, 10)
    print("scroolllled")

# Step 6: Check advance settings
    try:
        print("process 6 start")
        if wait_and_click(proxy_advanced_but_img, timeout=50, check_interval=4, confidence=0.9):
            time.sleep(2)  # Wait for the result to appear
            scroll_down_mouse(1)
            move_mouse_in_circle(2, 6)
            if wait_and_click(WebRTC_Replac_but_img, timeout=50, check_interval=4, confidence=0.9):
                move_mouse_in_circle(2, 6)
                wait_and_click(app_lang_togleButon_img, timeout=50, check_interval=4, confidence=0.9)
                move_mouse_in_circle(2, 6)
                wait_and_click(profile_creation_ok_but_img, timeout=50, check_interval=4, confidence=0.9)
    except Exception as e:
        print(f"An error occurred: {e}")
        return

def opning_profile(profile_readyToOpen_but_img):
    time.sleep(1)
    move_mouse_in_circle(5 , 20)
    try:
        if wait_and_click(profile_readyToOpen_but_img, timeout=60, check_interval=10, confidence=0.9):
            print("profile opning  button clicked successfully.")
            return 0
    except pyautogui.ImageNotFoundException as e:
        print(e)
        return


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
        return True
    else:
        if os.path.exists(exe_path):
            print(f"{window_title} window not found. Opening {executable_name}.")
            subprocess.Popen([exe_path])
            return True
        else:
            print(f"Error: {executable_name} not found at the specified path.")
            return False

def wait_for_window_to_load(window_title, timeout=60):
    start_time = time.time()
    while time.time() - start_time < timeout:
        if find_window_and_maximize(window_title):
            print(f"{window_title} window is open and ready.")
            return True
        time.sleep(1)
    print(f"Timeout: {window_title} window did not open in time.")
    return False

if __name__ == "__main__":
    curent_proxy = sys.argv[1]
    executable_name = "AdsPower Global.exe"
    window_title = "AdsPower"
    new_profile_button = "./images/new_profile_img.png"
    select_proxy_type = "./images/select_proxy_type_img.png"
    HTTPS_proxy_type_img = "./images/HTTPS_proxy_type_img.png"
    Socks5_proxy_type_img = "./images/Socks5_proxy_type_img.png"
    Host_Port_img = "./images/Host_Port_img.png"
    check_proxy_buton = "./images/check_proxy_buton_img.png"
    proxy_connection_failed_img = "./images/proxy_connection_failed_img.png"
    proxy_connection_success_img = "./images/proxy_connection_success_img.png"
    adsPower_back_but_img = "./images/adsPower_back_but_img.png"
    proxy_advanced_but_img = "./images/proxy_advanced_but_img.png"
    WebRTC_Replac_but_img = "./images/WebRTC_Replac_but_img.png"
    app_lang_togleButon_img = "./images/app_lang_togleButon_img.png"
    profile_creation_ok_but_img = "./images/profile_creation_ok_but_img.png"
    profile_readyToOpen_but_img = "./images/profile_readyToOpen_but_img.png"
    
# 01:profile creation in adsPower start
    # if open_executable_on_desktop(executable_name, window_title):
    #     if wait_for_window_to_load(window_title):
    #         create_profile(profile_creation_ok_but_img, app_lang_togleButon_img, WebRTC_Replac_but_img, proxy_advanced_but_img, adsPower_back_but_img, proxy_connection_failed_img, proxy_connection_success_img, check_proxy_buton, Host_Port_img, new_profile_button, select_proxy_type, HTTPS_proxy_type_img, Socks5_proxy_type_img, curent_proxy, attempts=5, delay_between_attempts=2)
    #     else:
    #         print("Failed to open AdsPower window in the allotted time.")
    # else:
    #     open_executable_on_desktop(executable_name, window_title)

# 01:profile opning after creation profile.
    opning_profile(profile_readyToOpen_but_img)
