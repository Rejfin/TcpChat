import socket
import threading

from colorama import initialise, Fore

# GLOBALS
HOST = "127.0.0.1"
PORT = 60453
ENCODE_FORMAT = "utf-8"
USERS = {}

initialise.init()


# try to create new connection at desire port and ip address
def main():
    print(f"Server started with ip {HOST} on port {PORT}")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sc:
        sc.bind((HOST, PORT))
        sc.listen()
        while True:
            conn, _ = sc.accept()

            # run separate thread for every single connection
            thread = threading.Thread(target=handle_connection, args=(conn,))
            thread.start()


def handle_connection(conn):
    with conn:
        try:
            # get nick of connecting user and save it to list of all users
            data = conn.recv(100).decode(ENCODE_FORMAT).split(':')
            if data[0].lower() == "nick":
                USERS[data[1].strip()] = conn
                print(f'Connected by: {conn.getsockname()[0]} nick: {data[1].strip()}')
                message_processing(f"{data[1].strip()} joined the chat")
                while True:
                    message_length = conn.recv(8)
                    message = conn.recv(int.from_bytes(message_length, 'big'))
                    message_processing(message.decode(ENCODE_FORMAT), data[1])
            else:
                conn.close()
                print(Fore.RED + f"connection with {conn.getsockname()[0]} terminated" + Fore.RESET)
        except Exception:
            # if exception is raised its mean user is disconnected from server
            print(Fore.RED + f"{data[1].strip()} has left the chat" + Fore.RESET)
            USERS.pop(data[1].strip())


# decided to send message to all users or to specific one
def message_processing(message, user=None):
    if user is None:
        broadcast_message(message)
    else:
        message = f"{user.strip()}: {message}"
        broadcast_message(message)


# send message to all users
def broadcast_message(message):
    for user in USERS.values():
        # send message length
        user.sendall(len(message.encode(ENCODE_FORMAT)).to_bytes(2, 'big'))
        # send message
        user.sendall(message.encode(ENCODE_FORMAT))


if __name__ == '__main__':
    main()
