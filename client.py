# telnet program
# does not work in IDLE

import sys, os

import socket, select, threading


def fetch_messages():
    while True:
        # Get the list sockets which are readable
        read_sockets, write_sockets, error_sockets = select.select([s], [], [])
        if read_sockets:
            # incoming message from remote server
            try:
                data = s.recv(4096)
            except:
                print('\nDisconnected from chat server')
                sys.exit()
            if data:
                print(data.decode("utf-8"))


def add_nt_input(input_queue):
    while True:
        input_queue.put(sys.stdin.read(1))


def send_message(message):
    if message != "\n":
        try:
            s.sendall(bytes(str(message), "utf-8"))
        except:
            print("Server does not respond")
            s.close()
            sys.exit()


def manage_user_input():
    if os.name == "nt":
        import queue
        input_queue = queue.Queue()
        input_thread = threading.Thread(target=add_nt_input,
                                        args=(input_queue,))
        input_thread.daemon = True
        input_thread.start()
        while True:
            message = ""
            while not input_queue.empty():
                message += input_queue.get()
            send_message(message)
    else:
        while True:
            message = sys.stdin.readline()
            send_message(message)

if __name__ == "__main__":
    host = '192.168.1.109'
    host = input("Please, specify IP address of the chat server: ")
    port = 8888
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
    # connect to remote host
    try:
        s.connect((host, port))
    except:
        print('Unable to connect')
        sys.exit()

    print('Connected to host. You can chat now.')
    threading.Thread(target=fetch_messages).start()
    manage_user_input()
