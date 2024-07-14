import os

def read_and_cut_first_proxy(file_path):
    proxy = None
    if os.path.exists(file_path):
        # Read all lines from the file
        with open(file_path, 'r') as file:
            lines = file.readlines()

        # If there are lines in the file, take the first one
        if lines:
            proxy = lines[0].strip()

            # Write remaining lines back to the file (excluding the first line)
            with open(file_path, 'w') as file:
                file.writelines(lines[1:])

        else:
            print(f"The file {file_path} is empty.")
    else:
        print(f"The file {file_path} does not exist.")

    return proxy

def read_keyWord_file_data(file_path):
    sentences_array = []

    if os.path.exists(file_path):
        # Read all lines from the file
        with open(file_path, 'r') as file:
            lines = file.readlines()

        # Strip any leading/trailing whitespace and add to the list
        sentences_array = [line.strip() for line in lines]

        if not sentences_array:
            print(f"The file {file_path} is empty.")
    else:
        print(f"The file {file_path} does not exist.")

    return sentences_array

# if __name__ == "__main__":
    # file_path = r"C:\Users\tosee\OneDrive\Desktop\proxy_data.txt"
    # proxy = read_and_cut_first_proxy(file_path)
    # print("Proxy:", proxy)
