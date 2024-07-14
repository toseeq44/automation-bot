import time
import sys
import os
import random
import pyautogui
from create_profile import wait_and_click, delet_profile_after_vist, move_mouse_in_circle, human_like_move_and_click
import pytesseract
from PIL import Image
import math
import socket
try:
    import win32con
    import win32gui
except ImportError as e:
    print(f"Import error: {e}")
    raise
import os
import fetching_files_data
import keyboard

first_call = True
pyautogui.FAILSAFE = False
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
desktop = r"C:\Users\tosee\OneDrive\Desktop"

# Helper function start =======================================================================================
def human_like_typing(text):
    for char in text:
        pyautogui.write(char)
        time.sleep(random.uniform(0.04, 0.1))

def smooth_scroll(offset):
    step = 100
    steps = abs(offset) // step
    for _ in range(steps):
        pyautogui.scroll(-step if offset > 0 else step)
        time.sleep(0.01)
    pyautogui.scroll(-offset % step if offset > 0 else offset % step)

def check_internet_connection():
    try:
        # Attempt to resolve Google's DNS to check internet connectivity
        socket.create_connection(("www.google.com", 80), timeout=5)
        return True
    except OSError:
        return False

def random_mouse_movement(duration=3):
    screen_width, screen_height = pyautogui.size()
    margin = 50  
    duration = duration  

    start_time = time.time()
    while time.time() - start_time < duration:
        
        direction = random.choice(['left', 'right', 'up', 'down', 'circle'])
        distance = random.randint(50, min(screen_width, screen_height) // 2)
        speed = random.uniform(0.1, 1)  
        current_x, current_y = pyautogui.position()
        if direction == 'left':
            new_x = max(margin, current_x - distance)
            new_y = current_y
        elif direction == 'right':
            new_x = min(screen_width - margin, current_x + distance)
            new_y = current_y
        elif direction == 'up':
            new_x = current_x
            new_y = max(margin, current_y - distance)
        elif direction == 'down':
            new_x = current_x
            new_y = min(screen_height - margin, current_y + distance)
        elif direction == 'circle':
            radius = random.randint(50, 150)
            angle = random.uniform(0, 2 * math.pi)
            new_x = min(max(margin, current_x + radius * math.cos(angle)), screen_width - margin)
            new_y = min(max(margin, current_y + radius * math.sin(angle)), screen_height - margin)

        pyautogui.moveTo(new_x, new_y, duration=speed)
        time.sleep(random.uniform(0.1, 0.5))

        if random.random() < 0.3:  # 30% chance to pause
            pause_duration = random.uniform(0.7, 2)
            time.sleep(pause_duration)

def move_mouse_randomly_within_area(top_pct=0.30, left_pct=0.20, right_pct=0.60, bottom_pct=0.80, duration=10):
    screen_width, screen_height = pyautogui.size()
    
    # Calculate the boundary coordinates
    top_boundary = int(screen_height * top_pct)
    left_boundary = int(screen_width * left_pct)
    right_boundary = int(screen_width * right_pct)
    bottom_boundary = int(screen_height * bottom_pct)
    
    start_time = time.time()

    while time.time() - start_time < duration:
        # Randomly select the direction
        direction = random.choice(['left_to_right', 'right_to_left', 'bottom_to_up', 'up_to_bottom'])
        
        if direction == 'left_to_right':
            start_x = left_boundary
            end_x = right_boundary
            y = random.randint(top_boundary, bottom_boundary)
            pyautogui.moveTo(start_x, y, duration=random.uniform(0.7, 1.5))
            pyautogui.moveTo(end_x, y, duration=random.uniform(0.7, 1.5))
        
        elif direction == 'right_to_left':
            start_x = right_boundary
            end_x = left_boundary
            y = random.randint(top_boundary, bottom_boundary)
            pyautogui.moveTo(start_x, y, duration=random.uniform(0.7, 1.5))
            pyautogui.moveTo(end_x, y, duration=random.uniform(0.7, 1.5))
        
        elif direction == 'bottom_to_up':
            start_y = bottom_boundary
            end_y = top_boundary
            x = random.randint(left_boundary, right_boundary)
            pyautogui.moveTo(x, start_y, duration=random.uniform(0.7, 1.5))
            pyautogui.moveTo(x, end_y, duration=random.uniform(0.7, 1.5))
        
        elif direction == 'up_to_bottom':
            start_y = top_boundary
            end_y = bottom_boundary
            x = random.randint(left_boundary, right_boundary)
            pyautogui.moveTo(x, start_y, duration=random.uniform(0.7, 1.5))
            pyautogui.moveTo(x, end_y, duration=random.uniform(0.7, 1.5))
        
        # Adding a small random delay to simulate reading time
        time.sleep(random.uniform(1, 2))

def check_and_open_google():
    global first_call
    pyautogui.hotkey('win', 'up')
    pyautogui.hotkey('ctrl', 't')
    time.sleep(1)
        
    if first_call:
        human_like_typing("https://www.google.com")
        pyautogui.press('enter')
        time.sleep(2)
        first_call = False 
    else:
        print("again call check_and_open_google function")

def search_keyword(keyword, image=None):
    random_mouse_movement(2)
    if image:
        location = pyautogui.locateOnScreen(image, confidence=0.9)
        if location:
            random_mouse_movement()
            pyautogui.moveTo(location)
            pyautogui.click()
    human_like_typing(keyword)
    pyautogui.press('enter')
    random_mouse_movement(4)

def close_popup():
    screen_width, screen_height = pyautogui.size()
    possible_popup_positions = [
        (screen_width // 2, screen_height // 2),
        (screen_width // 2, screen_height // 2 - 100),
        (screen_width // 2, screen_height // 2 + 100)
    ]
    for pos in possible_popup_positions:
        human_like_move_and_click(pos)
        random_mouse_movement(2) 

def spend_time_on_site():
    time_to_spend = random.randint(30, 50)
    print(f"Spending {time_to_spend} seconds on the site.")
    close_popup()
    
    clicked_on_word = False
    
    while time_to_spend > 0:
        scroll_time = min(time_to_spend, random.randint(5, 20))
        random_mouse_movement(scroll_time)
        time_to_spend -= scroll_time
        
        if random.choice([True, False]):
            # Scroll using mouse wheel
            pyautogui.scroll(-random.randint(200, 500))
        else:
            pyautogui.press('space')
        
        if not clicked_on_word and random.choice([True, False]):
            x, y = random.randint(100, pyautogui.size().width - 100), random.randint(100, pyautogui.size().height - 100)
            pyautogui.moveTo(x, y, duration=random.uniform(0.1, 0.5))
            if pyautogui.pixelMatchesColor(x, y, (255, 255, 255), tolerance=10):  # Adjust color and tolerance as needed
                pyautogui.click()
                print(f"Clicked at ({x}, {y}) on a random word.")
                clicked_on_word = True
        
        if random.choice([True, False]):
            pyautogui.hotkey('ctrl', 'c')
        if random.choice([True, False]):
            pyautogui.moveTo(random.randint(100, 800), random.randint(100, 600), duration=random.uniform(0.1, 0.5))
            pyautogui.click()
    
    print("Finished spending time on the site.")

def get_cursor_type():
    cursor = win32gui.GetCursorInfo()[1]
    arrow_cursor = win32gui.LoadCursor(0, win32con.IDC_ARROW)
    hand_cursor = win32gui.LoadCursor(0, win32con.IDC_HAND)
    if cursor == arrow_cursor:
        return 'Arrow'
    elif cursor == hand_cursor:
        return 'Hand'
    else:
        return 'Other'

def process_read_more_locations(read_more_button_images_locations):
    list_of_click_positions = []

    if len(read_more_button_images_locations) in [3, 4, 5, 6]:
        selected_locations = random.sample(read_more_button_images_locations, 3)
    else:
        num_to_select = random.randint(4, 6)
        selected_locations = random.sample(read_more_button_images_locations, num_to_select)

    list_of_click_positions.extend(selected_locations)
    return list_of_click_positions

def click_sponsored_link_by_id_with_offset(locations, link_id):
    print(f"1 call from click_sponsored_link_by_id_with_offset. location data: {locations}")

    if not locations:
        raise Exception("No locations found to click.")

    selected_location = random.choice(locations)
    link_id = selected_location['id']
    print(f"Selected link ID: {link_id}")

    pyautogui.scroll(1000)
    random_mouse_movement(2) 

    for loc in locations:
        if loc['id'] == link_id:
            x, y, width, height = loc['location']
            scroll_offset = loc['scroll_offset']
            print(f"2 call from click_sponsored_link_by_id_with_offset. Selected scroll offset: {scroll_offset}")

            pyautogui.scroll(-scroll_offset)
            random_mouse_movement(2) 

            final_x = x + width // 2
            final_y = y + height // 2 + 40

            pyautogui.moveTo(final_x, final_y)
            print(f"3 call from click_sponsored_link_by_id_with_offset. Clicking at: ({final_x}, {final_y})")
            pyautogui.click()
            spend_time_on_site()
            return

    raise Exception(f"Link with ID {link_id} not found.")

def collect_related_links_and_click():
    screen_width, screen_height = pyautogui.size()
    pointer_coordinates = []
    scroll_units = random.randint(300, 600)
    scroll_steps = scroll_units // 70  # Making smaller steps for smoother scrolling

    for _ in range(scroll_steps):  # Scroll in smaller steps for smoothness
        pyautogui.scroll(-25)
        time.sleep(0.02)  # Shorter sleep for smoother effect

        # Move the mouse in the specified range and check cursor type
        target_x = random.randint(int(0.10 * screen_width), int(0.30 * screen_width))
        target_y = random.randint(int(0.3 * screen_height), int(0.5 * screen_height))
        print(f"Specific area mouse movement {target_x} : {target_y}")
        pyautogui.moveTo(target_x, target_y, duration=0.2)

        # Check the current cursor icon, and if it's a pointer, save the coordinates
        cursor_type = get_cursor_type()
        print(f"Cursor info received: {cursor_type}")
        if cursor_type == 'Hand':  # Checking for the hand cursor type
            coordinate_info = {
                'id': len(pointer_coordinates) + 1,
                'x': target_x,
                'y': target_y,
                'offset_x': random.randint(-5, 5),
                'offset_y': random.randint(-5, 5)
            }
            pointer_coordinates.append(coordinate_info)

    # Scroll back up smoothly
    for _ in range(scroll_steps):
        pyautogui.scroll(20)
        time.sleep(0.03)

    # Randomly select a coordinate from the collected list
    if pointer_coordinates:
        chosen_coordinate = random.choice(pointer_coordinates)
        final_x = chosen_coordinate['x'] + chosen_coordinate['offset_x']
        final_y = chosen_coordinate['y'] + chosen_coordinate['offset_y']

        pyautogui.moveTo(final_x, final_y, duration=0.2)

        # Randomly choose to click or open in a new tab
        if random.choice([True, False]):
            pyautogui.click()
            spend_time_on_site()
        else:
            pyautogui.keyDown('ctrl')
            pyautogui.click(button='left')
            pyautogui.keyUp('ctrl')
            time.sleep(1)
            pyautogui.hotkey('ctrl', 'tab')
            spend_time_on_site()

def collect_sponsored_links_with_offsets(sponsored_link_img, scroll_pixels=500, max_scrolls=1):
    locations = []
    scroll_count = 0
    unique_id = 0
    current_scroll_offset = 0
    
    try:
        while scroll_count <= max_scrolls:
            found = list(pyautogui.locateAllOnScreen(sponsored_link_img))
            if not found:
                single_found = pyautogui.locateOnScreen(sponsored_link_img)
                if single_found:
                    found = [single_found]
            if found:
                for location in found:
                    x, y, width, height = location
                    locations.append({
                        'id': unique_id,
                        'location': (x, y, width, height),
                        'scroll_offset': current_scroll_offset
                    })
                    unique_id += 1
            else:
                print("No sponsored links found on the current screen.")
            pyautogui.scroll(-scroll_pixels)
            current_scroll_offset += scroll_pixels
            scroll_count += 1
        return locations

    except Exception as e:
        print(f"An error occurred: {e}")
        return []

def find_and_visit_sponsored_or_related_link(sponsored_link_img, keyword, open_link_in_new_tab_img, im_not_robot_img):
    print("find_and_visit_sponsored_or_related_link function start")
    try:
        # not_robot=pyautogui.locateOnScreen(im_not_robot_img)
        # if not_robot:
        #     return 1
        locations = collect_sponsored_links_with_offsets(sponsored_link_img)
        print(f"collect_sponsored_links_with_offsets function na loactions send ki ha :{locations}")
        num_links = len(locations)
        print(f"Number of sponsored links found: {num_links} and its type is {type(num_links)}")

        if num_links > 0:
            # Click on the first sponsored link
            click_sponsored_link_by_id_with_offset(locations, 0)
        else:
            print("No sponsored links found. Looking for related links...")
            collect_related_links_and_click()
    except Exception as e:
        print(e)
        return 0

def our_site(site_links):
    num_links = len(site_links)

    if num_links == 2:
        selected_links = site_links
    elif num_links == 5:
        num_to_select = random.randint(2, 5)
        selected_links = random.sample(site_links, num_to_select)
    elif num_links > 5:
        num_to_select = random.randint(2, 6)
        selected_links = random.sample(site_links, num_to_select)
    else:
        selected_links = site_links

    for link in selected_links:
        pyautogui.hotkey('ctrl', 't')
        random_mouse_movement(1)
        search_keyword(link)
        move_mouse_in_circle(4,20) 
        scroll_count = random.randint(11, 16)
        scrolls_done = 0

        while scrolls_done < scroll_count:
            initial_position = pyautogui.position()
            smooth_scroll(750)
            duration = random.randint(2, 5)
            move_mouse_randomly_within_area(top_pct=0.30, left_pct=0.20, right_pct=0.60, bottom_pct=0.80, duration=duration)
            current_position = pyautogui.position()
            print(f"Current position: {current_position}")
            if initial_position == current_position:
                break
            scrolls_done += 1
            print(f"Scrolls done: {scrolls_done}")

    pyautogui.hotkey('ctrl', 't')
        
# Helper function end =======================================================================================

# ====************* profile visiting code start ********************==========================

# Fetching data from keywords file
keyWords_data = sys.argv[1]
keywords_list = keyWords_data.split(',')
our_site_file_path = os.path.join(desktop, 'site_link.txt')
site_link = fetching_files_data.read_keyWord_file_data(our_site_file_path)
if site_link is None:
    print("Error: site_link file missing.")


script_code_file_path = os.path.join(desktop, 'script_code.txt')
script_code = fetching_files_data.read_keyWord_file_data(script_code_file_path)
if script_code is None:
    print("Error: site_link file missing.")

site_coord_file_path = os.path.join(desktop, 'site_coord.txt')



how_many_keyword_select = random.randint(4, 8)
print(f"Number of keywords to select from list: {how_many_keyword_select}")
selected_keywords = random.sample(keywords_list, how_many_keyword_select)
print("Selected keywords:", selected_keywords, type(selected_keywords))
second_search_num = random.randint(1, how_many_keyword_select // 2)
print(f"Number of keywords to select for second search: {second_search_num}")
second_search = random.sample(selected_keywords, second_search_num)
print("Second search keywords:", second_search)
first_search = [keyword for keyword in selected_keywords if keyword not in second_search]
print("First search keywords:", first_search)

# Profile visiting code start
google_search_area_img = "./images/google_search_area_img.png"
input_focus_img = "./images/input_focus_img.png"
sponsored_link_img = "./images/sponsored_link_img.png"
open_link_in_new_tab_img = "./images/open_link_in_new_tab_img.png"
read_more_img = "./images/read_more_img.png"
recent_post_img = "./images/recent_post_img.png"
google_popUp_img = "./images/google_popUp_img.png"
im_not_robot_img = "./images/im_not_robot_img.png"
dot_profile_info_img = "./images/dot_profile_info_img.png"
profile_delet_img = "./images/profile_delet_img.png"
clear_cachy_after_viste_frofile_img = "./images/clear_cachy_after_viste_frofile_img.png"
ok_button_for_cachy_caler_img = "./images/ok_button_for_cachy_caler_img.png"

# Start the process

if check_internet_connection():
    try:
        while first_search:
            check_and_open_google()
            keyword = first_search.pop(0)
            search_keyword(keyword)
            random_mouse_movement(3)
            find_and_visit_sponsored_or_related_link("sponsored_link_img", keyword, "open_link_in_new_tab_img", im_not_robot_img)
    except Exception as e:
        print(e)
    else:
        our_site(site_link) 
        while second_search:
            check_and_open_google()
            keyword = second_search.pop(0)
            search_keyword(keyword)
            random_mouse_movement(10)
            find_and_visit_sponsored_or_related_link("sponsored_link_img", keyword, "open_link_in_new_tab_img", im_not_robot_img)
        pyautogui.hotkey('alt', 'f4')
        delet_profile_after_vist(ok_button_for_cachy_caler_img, clear_cachy_after_viste_frofile_img, profile_delet_img, dot_profile_info_img)
else:
    print("Alert: No internet connection!")
