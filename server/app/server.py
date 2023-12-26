import socket

def start_server(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen()

        print(f"Server listening on {host}:{port}")

        while True:
            client_socket, addr = server_socket.accept()
            with client_socket:
                print(f"Connection from {addr}")
                client_socket.sendall(b"Hello from server!")

if __name__ == "__main__":
    HOST = '0.0.0.0'  # Standard loopback interface address (localhost)
    PORT = 9999        # Port to listen on

    start_server(HOST, PORT)
