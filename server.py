import socket

# サーバーのIPアドレスとポートを設定
server_ip = '127.0.0.1'
server_port = 8080

# ソケットを作成
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((server_ip, server_port))
server_socket.listen(5)
print(f"Server is waiting on {server_ip}:{server_port}...")

while True:
    # クライアントからの接続を受け入れ
    client_socket, client_address = server_socket.accept()
    print(f"connection established: {client_address}")

    # 送信するファイルの名前を受け取る
    requested_file = client_socket.recv(1024).decode('utf-8')
    print(f"requested file: {requested_file}")

    try:
        # ファイルを開いて読み込む
        with open(requested_file, 'rb') as file:
            # ファイルをクライアントに送信
            data = file.read()
            client_socket.sendall(data)
            print(f"{requested_file} successfully sent")
    except FileNotFoundError:
        print("file not found")
        client_socket.sendall(b"ERROR: File not found")

    # 接続を閉じる
    client_socket.close()
