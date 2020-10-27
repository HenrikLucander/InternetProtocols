import socket
import random
from collections import defaultdict


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


def get_sentence():
    """Function that creates a random sentence based on th principle of Markov chains

    :return:
    """
    with open("dracula.txt") as f:
        words = f.read().split()

    word_dict = defaultdict(list)
    for word, next_word in zip(words, words[1:]):
        word_dict[word].append(next_word)

    word = "Dracula"
    word_list = []
    while not word.endswith("."):
        word_list.append(word)
        word = random.choice(word_dict[word])

    _sentence = " ".join(word_list)
    return _sentence


class TCPClient:
    def __init__(self, host, port):
        self.serverName = host
        self.serverPort = port
        self.clientSocket = None

    def create(self):
        """Class method to create a TCP socket object and instantiates the clientSocket
        class variable

        """
        try:
            self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error as e:
            print(f"Error creating socket: {e}")

    def connect(self):
        """Class method to connect the client socket to given server ip address (serverName)
        and server port (serverPort).

        """
        try:
            self.clientSocket.connect((self.serverName, self.serverPort))
        except socket.error as e:
            print(f"Error creating socket: {e}")

    def send_message(self, sentence):
        """Class method to send a message from client to server

        :param sentence: The message (the sentence from client) that needs to be transmitted
        """
        try:
            self.clientSocket.send(encode_utf(sentence))
        except socket.error as e:
            print(f"Error sending data: {e}")

    def receive_message(self):
        """Class method to receive a message from server

        :return: The message returned from server
        :rtype: bytes
        """
        try:
            message = self.clientSocket.recv(1024)
            return message
        except socket.error as e:
            print(f"Error receiving data: {e}")

    def close_socket(self):
        """Method to close the created socket

        """
        self.clientSocket.close()

    def get_word_and_char_count(self, sentence_to_send):
        """The main driver mechanics that sends sentence to the server
        and return results from the server.

        :param sentence_to_send: The sentence to be send
        :type sentence_to_send: str
        :returns:
            - word_count - The number of words returned
            - num_chars - the number of characters returned
        """
        print(f"The sentence is: {sentence_to_send}")
        self.send_message(sentence_to_send)
        word_count, num_chars = [int(i) for i in decode_utf(self.receive_message()).split('\n')]
        print(f"The number of words is {word_count} and the characters is {num_chars}")
        return word_count, num_chars


if __name__ == '__main__':
    print("Client fired up:")
    serverName = socket.gethostname()  # ‘hostname’
    serverPort = 12000
    ip_address = socket.gethostbyname(serverName)
    client = TCPClient(ip_address, serverPort)
    client.create()
    client.connect()
    sentence = get_sentence()
    client.get_word_and_char_count(sentence)
    client.close_socket()
