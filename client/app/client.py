import socket

def connect_to_server(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((host, port))
        message = client_socket.recv(1024)
        print(f"Message from server: {message.decode()}")

if __name__ == "__main__":
    HOST = 'localhost'  # The server's hostname or IP address
    PORT = 9999         # The port used by the server

    connect_to_server(HOST, PORT)
