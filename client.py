import socket
import os
import http.client
import cv2
import numpy as np

# Function to get the global IP address without using requests
def get_global_ip():
    conn = http.client.HTTPConnection("api.ipify.org")
    conn.request("GET", "/")
    response = conn.getresponse()
    global_ip = response.read().decode('utf-8')
    return global_ip

SERVER_HOST = get_global_ip()
SERVER_PORT = 5001
BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"
DIRECTORY = "/Users/yu/Documents"  # Directory containing files to choose from

# Function to send the file to the server
def send_file(filepath):
    filename = os.path.basename(filepath)
    filesize = os.path.getsize(filepath)

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_HOST, SERVER_PORT))

    client_socket.send(f"{filename}{SEPARATOR}{filesize}".encode())

    with open(filepath, "rb") as f:
        while True:
            bytes_read = f.read(BUFFER_SIZE)
            if not bytes_read:
                break
            client_socket.sendall(bytes_read)

    client_socket.close()

# Function to handle mouse events and select file
def mouse_callback(event, x, y, flags, param):
    global file_list, selected_index
    if event == cv2.EVENT_LBUTTONDOWN:
        for i, (file, (fx, fy)) in enumerate(file_list):
            if fy < y < fy + 30 and fx < x < fx + 400:
                selected_index = i
                print(f"File selected: {file}")
                filepath = os.path.join(DIRECTORY, file)
                if os.path.isfile(filepath):
                    send_file(filepath)
                    print(f"Sent file: {file}")  # Debug print
                else:
                    print("File does not exist.")
                return

# Function to display a list of files and handle mouse clicks
def create_gui(file_list):
    global selected_index
    selected_index = -1

    # Prepare file list positions
    positions = [(50, 150 + i * 30) for i in range(len(file_list))]
    file_list_with_positions = list(zip(file_list, positions))

    cv2.namedWindow("FilePass Client")
    cv2.setMouseCallback("FilePass Client", mouse_callback)

    while True:
        frame = np.zeros((400, 600, 3), dtype="uint8")
        cv2.putText(frame, "FilePass Client", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv2.putText(frame, "Select a file:", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 1)

        # Display file list
        for i, (file, (fx, fy)) in enumerate(file_list_with_positions):
            color = (0, 255, 0) if i == selected_index else (255, 255, 255)
            cv2.putText(frame, file, (fx, fy), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 1)

        cv2.imshow("FilePass Client", frame)

        key = cv2.waitKey(10)  # Check for key events
        if key == 27:  # Escape key
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    # Get list of files from the directory
    if not os.path.exists(DIRECTORY):
        os.makedirs(DIRECTORY)
    file_list = [f for f in os.listdir(DIRECTORY) if os.path.isfile(os.path.join(DIRECTORY, f))]

    if file_list:
        print(f"Files available for selection: {file_list}")  # Debug print
        create_gui(file_list)
    else:
        print("No files found in the directory.")
