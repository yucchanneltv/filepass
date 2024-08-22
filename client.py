import socket

# サーバーのIPアドレスとポートを設定
server_ip = '127.0.0.1'
server_port = 5000

# ソケットを作成
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((server_ip, server_port))

# 要求するファイルの名前を入力
requested_file = input("Please enter the file name to download: ")
client_socket.sendall(requested_file.encode('utf-8'))

# サーバーからのデータを受け取る
file_data = client_socket.recv(1024)

# ファイルが見つかった場合、データをファイルに書き込む
if file_data.startswith(b"ERROR"):
    print(file_data.decode('utf-8'))
else:
    with open(f"downloaded_{requested_file}", 'wb') as file:
        file.write(file_data)
    print(f"{requested_file} downloaded")

# 接続を閉じる
client_socket.close()
