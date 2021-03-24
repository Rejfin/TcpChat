import socket
import threading
from colorama import initialise, Fore

HOST = '192.168.0.152'
PORT = 60453
ENCODE_FORMAT = "utf-8"

initialise.init()
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))


def receive_message():
    try:
        while True:
            message_length = client.recv(8)
            message = client.recv(int.from_bytes(message_length, 'big')).decode(ENCODE_FORMAT)

            if "joined the chat" in message:
                print(Fore.YELLOW + message + Fore.RESET)
            else:
                print(message)
    except Exception:
        print("disconnected from server")
        # TODO DO SOMETHING


def write_message():
    while True:
        message = input()
        # send message length
        client.sendall(len(message.encode(ENCODE_FORMAT)).to_bytes(2, 'big'))
        # send message
        client.sendall(message.encode(ENCODE_FORMAT))


def main():
    thread1 = threading.Thread(target=receive_message)
    thread1.start()

    nick = input("nick: ")
    client.send(f"nick:{nick}".encode(ENCODE_FORMAT))

    thread2 = threading.Thread(target=write_message())
    thread2.start()


main()



