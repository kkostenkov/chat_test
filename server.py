# Chat server

import socket, select


# Function to broadcast chat messages to all connected clients
def broadcast_data(sender, message):
    byte_message = bytes(message, 'UTF-8')
    # print("broadcasting", len(connection_list))
    # Do not send the message to master socket
    # and the client who has send us the message
    for socket in connection_list:
        if socket != server_socket and socket != sender:
            try:
                socket.send(byte_message)
            except:
                # handle broken socket connections
                socket.close()
                connection_list.remove(socket)

if __name__ == "__main__":
    # List to keep track of socket descriptors
    connection_list = []
    PORT = 8888
    RECV_BUFFER = 4096

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("0.0.0.0", PORT))
    server_socket.listen(10)
    # Add server socket to the list of readable connections
    connection_list.append(server_socket)
    print("Chat server started on port %s" % str(PORT))
    server_running = True
    while server_running:
        # Get the list sockets which are ready to be read through select
        read_sockets = select.select(connection_list, [], [])[0]
        for socket in read_sockets:
            # New connection
            if socket == server_socket:
                # A new connection recieved through server_socket
                new_sock, addr = server_socket.accept()
                connection_list.append(new_sock)
                print("Client (%s, %s) connected" % addr)
                broadcast_data(new_sock, "[%s:%s] entered room\n" % addr)
            # Incoming message from a client
            else:
                try:
                    data = socket.recv(RECV_BUFFER).decode('utf-8')
                except:
                    broadcast_data(socket, "Client (%s, %s) is offline\n" % addr)
                    print("Client (%s, %s) is offline" % addr)
                    socket.close()
                    connection_list.remove(socket)
                    continue
                if data:
                    formatted_message = "<{0}> {1}".format(socket.getpeername()[0], data)
                    print(formatted_message)
                    broadcast_data(socket, formatted_message)
    server_socket.close()
