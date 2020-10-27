import socket


def set_port_ip():
    server_port_ = 12000                            # ""  # TODO: Complete the port here
    server_name = socket.gethostname()              # ""  # TODO: Get the server name
    ip_address_ = socket.gethostbyname(server_name)    # ""  # TODO: Get the server ip address
    return server_port_, ip_address_


def encode_utf(message):
    """Encodes a given message to utf-8 encoding

    :param message: The message to be encoded to utf-8
    :type message: str
    :return: The utf-8 encoded message
    """
    return str(message).encode('utf-8')


def decode_utf(message):
    """Decodes a given message from utf-8 encoding

    :param message: The message to be decoded to utf-8
    :return: The utf-8 decoded message
    """
    return message.decode('utf-8')


def count_words(sentence_):
    """Count the number of words in a given sentence

    :param sentence_: Input sentence for counting words
    :type sentence_: str
    :return: word count in input sentence
    :rtype: int
    """
    return len(sentence_.split())


def count_chars(sentence_):
    """Count the number of characters in a given sentence

    :param sentence_: Input sentence for counting characters
    :type sentence_: str
    :return: character count in input sentence
    :rtype: int
    """
    return len(sentence_) - sentence_.count(' ')


class TCPServer:
    def __init__(self, ip, port_name):
        self.host = ip
        self.serverPort = port_name
        self.serverSocket = None
        self.connectionSocket = None

    def create(self):
        """Method creates a TCP socket and instantiates the class variable serverSocket.

        """
        try:
            self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #"" # TODO: Remove empty string and create a new TCP socket here
            self.serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        except socket.error as e:
            print(f"Error creating socket: {e}")

    def bind_and_listen(self):
        """Method binds the created socket to the hostname (host) and port (serverPort), and finally listens to the
        serverSocket.
        """
        try:
            print("Bind and Listen")
            # TODO: Bind the created socket (serverSocket) to the ip address (host) and port (serverPort)
            self.serverSocket.bind((self.host, self.serverPort))
            # TODO: listen to the serverSocket for connections. Set backlog=1.
            self.serverSocket.listen(1) #listen(backlog) = how many connections can be hold in queue
        except socket.error as e:
            print(f"Error creating socket: {e}")

    def accept_connection(self):
        """Method to accept the TCP connection from the client

        :returns:
            - connection_socket - A new socket object usable to send and receive data on the connection
            - address -  Address bound to the socket on the client
        """
        try:
            connection_socket, addr = self.serverSocket.accept() #""  # TODO: Accept an incoming connection
            return connection_socket, addr
        except socket.error as e:
            print(f"Error receiving message: {e}")

    def receive_message(self):
        """Class method to receive a message (the sentence) from client

        :return: The received sentence from the client
        """
        try:
           # sentence = self.serverSocket.recv(1024) # TODO: Utilize the serverSocket to receive the message from the client.
            sentence = self.connectionSocket.recv(1024)
            return sentence
        except socket.error as e:
            print(f"Error receiving message: {e}")

    def send_message(self, word_count, num_chars):
        """Class method to send a message from server to client

        :param word_count: The number of words counted
        :param num_chars: The number of characters counted
        """
        message_to_send = encode_utf("\n".join([str(word_count), str(num_chars)]))
        self.connectionSocket.send(message_to_send) # TODO: Use the created serverSocket to send the above given encoded message (message_to_send) to client

    def close_socket(self):
        """Method to close the created socket

        """
        self.serverSocket.close()

    def find_words_and_chars(self):
        """The main back-end mechanics of the Server. Receives the sentence, finds the number
        of words and characters and sends it back to client.

        """
        breakout = True
        while breakout:
            self.connectionSocket, addr = self.accept_connection()
            sentence = self.receive_message()
            sentence = decode_utf(sentence)
            word_count = count_words(sentence)
            num_chars = count_chars(sentence)
            if str(word_count).isdigit() and str(num_chars).isdigit():
                breakout = False
            self.send_message(word_count, num_chars)
            self.connectionSocket.close()
        # self.close_socket()


if __name__ == '__main__':
    print("Server fired up:")
    port, host = set_port_ip()
    server = TCPServer(host, port)
    server.create()
    server.bind_and_listen()
    server.find_words_and_chars()
    server.close_socket()
