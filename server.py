import socket
import threading
import os
import cv2
import numpy as np
import http.client

# Function to get the global IP address without using requests
def get_global_ip():
    conn = http.client.HTTPConnection("api.ipify.org")
    conn.request("GET", "/")
    response = conn.getresponse()
    global_ip = response.read().decode()
    conn.close()
    return global_ip

# Automatically get the global IP address
SERVER_HOST = get_global_ip()
SERVER_PORT = 5001
BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"

# Directory to store received files
RECEIVE_DIR = "received_files"

# Create the directory if it doesn't exist
os.makedirs(RECEIVE_DIR, exist_ok=True)

def handle_client(client_socket):
    try:
        # Receive the file details
        received = client_socket.recv(BUFFER_SIZE).decode()
        filename, filesize = received.split(SEPARATOR)
        filename = os.path.basename(filename)
        filesize = int(filesize)

        # Save the received file to the specified directory
        filepath = os.path.join(RECEIVE_DIR, filename)
        with open(filepath, "wb") as f:
            while True:
                bytes_read = client_socket.recv(BUFFER_SIZE)
                if not bytes_read:
                    break
                f.write(bytes_read)

        print(f"File received: {filename}")

    finally:
        client_socket.close()

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen(5)
    print(f"[*] Listening on {SERVER_HOST}:{SERVER_PORT}")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"[+] {addr} connected.")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

def create_gui():
    while True:
        frame = np.zeros((300, 500, 3), dtype="uint8")
        cv2.putText(frame, "FilePass Server 2024", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv2.putText(frame, f"Server IP: {SERVER_HOST}", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(frame, f"Port: {SERVER_PORT}", (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(frame, "Waiting for connections...", (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        cv2.imshow("FilePass Server", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    server_thread = threading.Thread(target=start_server)
    server_thread.start()

    create_gui()
